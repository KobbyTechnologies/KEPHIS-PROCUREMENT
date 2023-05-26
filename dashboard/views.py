from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from myRequest.views import UserObjectMixin

# Create your views here.


def canvas(request):
    state = request.session['state']

    ctx = {"state": state}

    return render(request, 'offcanvas.html', ctx)


class dashboard(UserObjectMixin,View):
    def get(self, request):
        try:
            name=request.session['FullName']
            state = request.session['state']
            proc_methods =self.logical_triple_filter("/ProcurementMethods","Status","eq","New")
            open_tenders = [x for x in proc_methods[1] if x['TenderType'] == 'Open Tender']
            restricted_tenders = [x for x in proc_methods[1] if x['TenderType'] == "Restricted Tender"]
            rfq = [x for x in proc_methods[1] if x['Process_Type'] == 'RFQ']
            eoi = [x for x in proc_methods[1] if x['Process_Type'] == 'EOI']

            closed = self.one_filter("/ProcurementMethods","Status","eq","Archived")
            new = self.one_filter("/ProcurementMethods","Status","eq","New")

            tender_responses = self.one_filter("/QyProspectiveSupplierTender","Vendor_No","eq",request.session['UserId'])
            EOI_Active = [x for x in tender_responses[1] if x['Type'] == 'EOI']
            RFQ_Active = [x for x in tender_responses[1] if x['Type'] == 'RFQ']
            RFP_Active = [x for x in tender_responses[1] if x['Type'] == 'RFP']
            RES_Active = [x for x in tender_responses[1] if x['Type'] == 'Restricted']
            Active_O = [x for x in tender_responses[1] if x['Type'] == 'Tender']
            print(tender_responses)

            ctx = {
                "state": state,"today":self.todays_date,
                "open_tenders":open_tenders,
                "restricted_tenders":restricted_tenders,
                "rfq":rfq,"eoi":eoi,"Close":closed[0], "Actives": new[0],
                "RES_A": RES_Active,"RFP_A": RFP_Active, "Active_O": Active_O,
                "RFQ_A": RFQ_Active,"EOI_A": EOI_Active,
                'fullname': name,
            }
        except Exception as e:
            print(e)
            messages.error(request,f"{e}")
            return redirect('login')
        return render(request, 'main/dashboard.html',ctx)
