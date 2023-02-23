from django.shortcuts import render, redirect
from datetime import date
import requests
from requests import Session
from requests_ntlm import HttpNtlmAuth
import json
from django.conf import settings as config
import datetime
from requests.adapters import HTTPAdapter
from django.contrib import messages
import base64
from django.http import HttpResponse
import io as BytesIO

# Create your views here.


def open_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access = config.O_DATA.format("/QyProspectiveSupplierTender")
    open = ''
    Submitted = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        responses = session.get(Access, timeout=10).json()
        open = []
        Submitted = []

        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender' and tender['SubmittedToPortal'] == True and tender['Status'] == 'Approved':
                output_json = json.dumps(tender)
                open.append(json.loads(output_json))

        for tender in responses['value']:
            if tender['Type'] == 'Tender' and tender['Vendor_No'] == request.session['UserId']:
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))

    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(open)
    counter = len(Submitted)
    # Get Timezone
    # creating date object
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    states = request.session['state']
    print(states)

    ctx = {"today": todays_date, "res": open,
           "count": count, "counter": counter, "sub": Submitted,
           "states": states}
    return render(request, 'openTenders.html', ctx)


def Open_Details(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access2 = config.O_DATA.format("/ProcurementRequiredDocs")
    lines = config.O_DATA.format("/ProcurementMethodLines")
    Access_File = config.O_DATA.format("/QyDocumentAttachments")

    res = ''
    State = ''
    instruct = ""
    files = ""
    Doc = ''
    Lines = ''
    allFiles = ''
    try:
        r = session.get(Access2, timeout=7).json()
        response = session.get(Access_Point, timeout=8).json()
        lines_res = session.get(lines, timeout=8).json()
        Open = []
        Doc = []
        Lines = []
        for lines in lines_res['value']:
            if lines['RequisitionNo'] == pk:
                output_json = json.dumps(lines)
                Lines.append(json.loads(output_json))
                # print(Lines)
        for tender in response['value']:
            if tender['No'] == pk:
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
                    if my_tender['No'] == pk:
                        res = my_tender
                        instruct = my_tender['Instructions']
                    if my_tender['Status'] == "New":
                        State = 1
        for docs in r['value']:
            if docs['QuoteNo'] == pk:
                output_json = json.dumps(docs)
                Doc.append(json.loads(output_json))

    except requests.exceptions.ConnectionError as e:
        print(e)
    try:
        allFiles = []
        res_file = session.get(Access_File, timeout=10).json()
        for tender in res_file['value']:
            if tender['No_'] == pk:
                output_json = json.dumps(tender)
                allFiles.append(json.loads(output_json))
    except Exception as e:
        print(e)

    if request.method == 'POST':
        docNo = pk
        attachmentID = request.POST.get('attachmentID')
        File_Name = request.POST.get('File_Name')
        File_Extension = request.POST.get('File_Extension')
        tableID = 52177788

        try:
            response = config.CLIENT.service.FnGetDocumentAttachment(
                docNo, attachmentID, tableID)

            filenameFromApp = File_Name + "." + File_Extension
            buffer = BytesIO.BytesIO()
            content = base64.b64decode(response)
            buffer.write(content)
            responses = HttpResponse(
                buffer.getvalue(),
                content_type="application/ms-excel",
            )
            responses['Content-Disposition'] = f'inline;filename={filenameFromApp}'
            return responses
        except Exception as e:
            messages.error(request, f'{e}')
            print(e)
        return redirect('Odetails', pk=docNo)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    states = request.session['state']
    ctx = {"today": todays_date, "res": res,
           "docs": Doc, "state": State,
           "line": Lines,
           "instruct": instruct, "file": allFiles,
           "states": states}
    return render(request, "details/open.html", ctx)


def DocResponse(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    procurementMethod = ''
    docNo = ''
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=8).json()

        Open = []
        for tender in response['value']:
            if tender['No'] == pk:
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender':
                        procurementMethod = 1
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender":
                        procurementMethod = 5
                    if tender['Process_Type'] == 'RFQ':
                        procurementMethod = 2
                    if tender['Process_Type'] == 'EOI':
                        procurementMethod = 4
                    if tender['Process_Type'] == 'RFP':
                        procurementMethod = 3
    except requests.exceptions.ConnectionError as e:
        print(e)

    if request.session['state'] == 'Vendor':

        vendNo = request.session['UserId']
        docNo = pk
        unitPrice = ''
        userType = 'vendor'

        if request.method == "POST":
            try:
                myAction = request.POST.get('myAction')
                responseNo = request.POST.get('responseNo')
                unitPrice = float(request.POST.get('amount'))
            except ValueError:
                messages.error(request, "Invalid Amount, Try Again!!")
                return redirect('Odetails', pk=docNo)
            try:
                if vendNo != '':
                    result = config.CLIENT.service.FnCreateProspectiveSupplier(myAction, responseNo,
                                                                               vendNo, procurementMethod, docNo, unitPrice, userType)
                    print(result)
                    # if result:
                    #     request.session['ProNumber'] = result

                    #     ProNumber = request.session['ProNumber']

                    if result == True:

                        messages.success(
                            request, f"You have successfully Applied for Doc number {docNo}")
                        return redirect('Odetails', pk=docNo)
            except Exception as e:
                messages.error(request, f'{e}')
                print(e)

    if request.session['state'] == 'Prospect':

        vendNo = request.session['UserId']
        docNo = pk
        unitPrice = ''
        userType = 'prospective'

        if request.method == "POST":
            try:
                myAction = request.POST.get('myAction')
                responseNo = request.POST.get('responseNo')
                unitPrice = float(request.POST.get('amount'))
            except ValueError:
                messages.error(request, "Invalid Amount, Try Again!!")
                return redirect('Odetails', pk=docNo)
            print(vendNo)
            print(docNo)
            print(unitPrice)
            print(userType)
            try:
                if vendNo != '':
                    result = config.CLIENT.service.FnCreateProspectiveSupplier(
                        myAction, responseNo, vendNo, procurementMethod, docNo, unitPrice, userType
                    )
                    print("result", result)
                    # if result:
                    #     request.session['ProNumber'] = result
                    if result == True:
                        messages.success(
                            request, f"You have successfully Applied for Doc number {docNo}")
                        return redirect('Odetails', pk=docNo)

                    elif result == False:
                        messages.error(request, f'{result}')
                        return redirect('Odetails', pk=docNo)
                    else:
                        messages.error(request, f'{result}')
                        return redirect('Odetails', pk=docNo)

            except Exception as e:
                messages.error(request, f"{e}")
                print(e)
    return redirect('Odetails', pk=docNo)


def fnCreateprospectiveSupplierTender(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    procurementMethod = ''
    Access_Point = config.O_DATA.format("/ProcurementMethods")
    try:
        response = session.get(Access_Point, timeout=8).json()

        Open = []
        for tender in response['value']:
            if tender['No'] == pk:
                output_json = json.dumps(tender)
                Open.append(json.loads(output_json))
                responses = Open
                for my_tender in responses:
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == 'Open Tender':
                        procurementMethod = 1
                    if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender":
                        procurementMethod = 5
                    if tender['Process_Type'] == 'RFQ':
                        procurementMethod = 2
                    if tender['Process_Type'] == 'EOI':
                        procurementMethod = 4
                    if tender['Process_Type'] == 'RFP':
                        procurementMethod = 3
    except requests.exceptions.ConnectionError as e:
        print(e)
    if request.method == 'POST':
        try:
            prospectNo = ''
            vendorNo = ''

            if request.session['state'] == 'Prospect':
                prospectNo = request.session['UserId']

            elif request.session['state'] == 'Vendor':
                vendorNo = request.session('UserId')

            myAction = request.POST.get('myAction')

            tenderNo = request.POST.get('tenderNo')

            print('prospectNo;', prospectNo)
            print("vendorNo:", vendorNo)
            print('procurementMethod:', procurementMethod)
            print('tenderNo', tenderNo)
            print('myAction:', myAction)

            response = config.CLIENT.service.fnCreateprospectiveSupplierTender(
                myAction, prospectNo, procurementMethod, tenderNo, vendorNo)

            if response == True:
                messages.success(
                    request, f'successful proceed to add your quoted amount')
                return redirect('Odetails', pk=pk)
            elif response == False:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
            else:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
        except Exception as e:
            messages.error(request, f'{e}')
            redirect('Odetails', pk=pk)

    return redirect('Odetails', pk=pk)


def fnCreateProspectiveTenderLine(request, pk):
    if request.method == 'POST':
        try:
            prospectNo = ''
            vendorNo = ''
            if request.session['state'] == 'Prospect':
                prospectNo = request.session['UserId']

            elif request.session['state'] == 'Vendor':
                vendorNo = request.session('UserId')

            tenderNo = request.POST.get('tenderNo')
            amount = request.POST.get('amount')

            print('prospectNo;', prospectNo)
            print("vendorNo:", vendorNo)
            print('tenderNo', tenderNo)
            print('Amount:', amount)

            response = config.CLIENT.service.fnCreateprospectiveSupplierTender(
                prospectNo, vendorNo, tenderNo, amount)

            if response == True:
                messages.success(
                    request, f'successful proceed to add your quoted amount')
                return redirect('Odetails', pk=pk)
            elif response == False:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
            else:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
        except Exception as e:
            messages.error(request, f'{e}')
            redirect('Odetails', pk=pk)

    return redirect('Odetails', pk=pk)


def fnModifyProspectiveTenderLine(request, pk):
    if request.method == 'POST':
        try:
            vendorNo = ''
            prospectNo = ''
            if request.session['state'] == 'Prospect':
                prospectNo = request.session['UserId']

            elif request.session['state'] == 'Vendor':
                vendorNo = request.session('UserId')

            amount = request.POST.get('amount')
            lineNo = request.POST.get('lineNo')
            tenderNo = request.POST.get('tenderNo')

            response = config.CLIENT.service.fnCreateprospectiveSupplierTender(
                prospectNo, vendorNo, lineNo, tenderNo, amount)
            if response == True:
                messages.success(
                    request, f'successful proceed to add your quoted amount')
                return redirect('Odetails', pk=pk)
            elif response == False:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
            else:
                messages.error(request, f'Something went wrong! Try again.')
                return redirect('Odetails', pk=pk)
        except Exception as e:
            messages.error(request, f'{e}')
            redirect('Odetails', pk=pk)

    return redirect('Odetails', pk=pk)


def fnInsertSuppliersToProcurementMethod(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access_Point = config.O_DATA.format("/ProcurementMethods")

    try:
        response = session.get(Access_Point, timeout=8).json()

        if request.method == 'POST':
            try:
                referenceNo = request.POST.get('referenceNo')
                supplierCode = request.session['UserId']

                response = config.CLIENT.service.fnInsertSuppliersToProcurementMethod(
                    referenceNo, supplierCode
                )
                if response == True:
                    messages.success(
                        request, "Submitted successfully for review")
                    return redirect('Odetails', pk=pk)
                else:
                    messages.error(request, "Failed, Try Again")
                    return redirect('Odetails', pk=pk)
            except Exception as e:
                messages.error(request, f'{e}')
                redirect('Odetails', pk=pk)
    except Exception as e:
        messages.error(request, f'{e}')
        redirect('Odetails', pk=pk)

    return redirect('Odetails', pk=pk)


def Restricted_tenders(request):
    session = requests.Session()
    session.auth = config.AUTHS

    Access_Point = config.O_DATA.format("/ProcurementMethods")
    Access = config.O_DATA.format("/QyProspectiveSupplierTender")
    Restrict = ''
    Submitted = ''
    try:
        response = session.get(Access_Point, timeout=10).json()
        responses = session.get(Access, timeout=10).json()
        Restrict = []
        Submitted = []
        for tender in response['value']:
            if tender['Process_Type'] == 'Tender' and tender['TenderType'] == "Restricted Tender" and tender['Status'] == 'New':
                output_json = json.dumps(tender)
                Restrict.append(json.loads(output_json))
        for tender in responses['value']:
            if tender['Type'] == 'Restricted' and tender['Vendor_No'] == request.session['UserId']:
                output_json = json.dumps(tender)
                Submitted.append(json.loads(output_json))
    except requests.exceptions.ConnectionError as e:
        print(e)

    count = len(Restrict)
    counter = len(Submitted)

    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    ctx = {"today": todays_date, "res": Restrict,
           "count": count, "sub": Submitted, "counter": counter}
    return render(request, 'restrictedTenders.html', ctx)


def UploadAttachedDocument(request, pk):

    session = requests.Session()
    response = request.session['UserId']
    fileName = ""
    attachment = ""
    vendorNo = response
    myUserId = response
    # tableID = 52177763 get checklist
    tableID = 52177788

    if request.method == "POST":
        try:
            attach = request.FILES.getlist('attachment')
        except Exception as e:
            print("Not Working")
            return redirect('Odetails', pk=pk)
        for files in attach:
            fileName = request.FILES['attachment'].name
            attachment = base64.b64encode(files.read())

            try:
                response = config.CLIENT.service.FnUploadProspectiveLineAttachedDocument(
                    pk, fileName, attachment, tableID, myUserId, vendorNo, pk)
            except Exception as e:
                messages.error(request, f"{e}")
                print(e)
        if response == True:
            messages.success(request, "Successfully Sent !!")
            return redirect('Odetails', pk=pk)
        else:
            messages.error(request, "Not Sent !!")
            return redirect('Odetails', pk=pk)

    return redirect('Odetails', pk=pk)


def submitted(request, pk):
    session = requests.Session()
    session.auth = config.AUTHS
    Access = config.O_DATA.format("/QyProspectiveSupplierTender")
    res = " "
    try:
        response = session.get(Access, timeout=8).json()
        for tender in response['value']:
            if tender['Tender_No_'] == pk and tender['Vendor_No'] == request.session['UserId']:
                res = tender
    except requests.exceptions.ConnectionError as e:
        print(e)
    todays_date = datetime.datetime.now().strftime("%b. %d, %Y %A")
    states = request.session['state']
    ctx = {"res": res,
           "today": todays_date, "states": states}
    return render(request, "details/submitted.html", ctx)
