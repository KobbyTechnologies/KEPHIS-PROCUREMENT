document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId)

        // Validate that all variables exist
        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
                // show navbar
                nav.classList.toggle('shows')
                // change icon
                toggle.classList.toggle('las-la')
                // add padding to body
                bodypd.classList.toggle('body-pds')
                // add padding to header
                headerpd.classList.toggle('body-pds')
            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header')

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink() {
        if (linkColor) {
            linkColor.forEach(l => l.classList.remove('active'))
            this.classList.add('active')
        }
    }
    linkColor.forEach(l => l.addEventListener('click', colorLink))

    // Your code to run since DOM is loaded and ready
});
$(document).ready(function () {
    $("#nav-bar").addClass('shows');
    $("#header").addClass('body-pds');
    $("#body-pd").addClass('body-pds');
    $("#nav-bar").hover(function (e) {
        e.preventDefault();
        $("#nav-bar").addClass('shows');
        $("#header").addClass('body-pds');
        $("#body-pd").addClass('body-pds');
        $("#nav_p").show();
        $('.nav::-webkit-scrollbar').show(500)

    })
    $("#header-toggle").click(function (e) {
        e.preventDefault();
        $("#nav_p").hide();
    })
    $("#pop2").popover({
        trigger: "hover"
    });
    $("#pop3").popover({
        trigger: "hover"
    });
    $("#pop4").popover({
        trigger: "hover"
    });
    $("#pop5").popover({
        trigger: "hover"
    });
    $("#pop6").popover({
        trigger: "hover"
    });
    $("#pop7").popover({
        trigger: "hover"
    });
    $("#res_card").removeClass('t-card')

    $("#filebtn").click(function () {
        $("#file_up").toggle(500)
    })
    $("#showForm").click(function () {
        $("#formContainer").toggle(500)
    })
    $("#reg").click(function (e) {
        e.preventDefault();
        $("#n-right1").hide();
        $("#n-right2").show();
    })
    $("#log").click(function (e) {
        e.preventDefault();
        $("#n-right2").hide();
        $("#n-right1").show();
    })
})
// menu
// popovers Initialization
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})

$(document).ready(function () {
    var table = $('#example').DataTable({
        select: true,
        paging: false,
        scrollX: false,
        scrollY: '50vh',
        scrollCollapse: true,
    });
    new $.fn.dataTable.FixedHeader(table);
});

// wizard
const nxtBtn = document.querySelector('#submitBtn');
const form1 = document.querySelector('#form1');
const form2 = document.querySelector('#form2');
const form3 = document.querySelector('#form3');
const form4 = document.querySelector('#form4');
const form5 = document.querySelector('#form5');


const icon1 = document.querySelector('#icon1');
const icon2 = document.querySelector('#icon2');
const icon3 = document.querySelector('#icon3');
const icon4 = document.querySelector('#icon4');
const icon5 = document.querySelector('#icon5');


var viewId = 1;

function nextForm() {
    console.log("hellonext");
    viewId = viewId + 1;
    progressBar();
    displayForms();

    console.log(viewId);

}

function prevForm() {
    console.log("helloprev");
    viewId = viewId - 1;
    console.log(viewId);
    progressBar1();
    displayForms();
}

function progressBar1() {
    if (viewId === 1) {
        icon2.classList.add('active');
        icon2.classList.remove('active');
        icon3.classList.remove('active');
        icon4.classList.remove('active');
        icon5.classList.remove('active');
    }
    if (viewId === 2) {
        icon2.classList.add('active');
        icon3.classList.remove('active');
        icon4.classList.remove('active');
        icon5.classList.remove('active');
    }
    if (viewId === 3) {
        icon3.classList.add('active');
        icon4.classList.remove('active');
        icon5.classList.remove('active');
    }
    if (viewId === 4) {
        icon4.classList.add('active');
        icon5.classList.remove('active');
    }
    if (viewId === 5) {
        icon5.classList.add('active');
        nxtBtn.innerHTML = "Submit"
    }
    if (viewId > 5) {
        icon2.classList.remove('active');
        icon3.classList.remove('active');
        icon4.classList.remove('active');
        icon5.classList.remove('active');

    }
}

function progressBar() {
    if (viewId === 2) {
        icon2.classList.add('active');
    }
    if (viewId === 3) {
        icon3.classList.add('active');
    }
    if (viewId === 4) {
        icon4.classList.add('active');
    }
    if (viewId === 5) {
        icon5.classList.add('active');
        nxtBtn.innerHTML = "Submit"
    }
    if (viewId > 5) {
        icon2.classList.remove('active');
        icon3.classList.remove('active');
        icon4.classList.remove('active');
        icon5.classList.remove('active');

    }
}

function displayForms() {

    if (viewId > 5) {
        viewId = 1;
    }

    if (viewId === 1) {
        form1.style.display = 'block';
        form2.style.display = 'none';
        form3.style.display = 'none';
        form4.style.display = 'none';
        form5.style.display = 'none';


    } else if (viewId === 2) {
        form1.style.display = 'none';
        form2.style.display = 'block';
        form3.style.display = 'none';
        form4.style.display = 'none';
        form5.style.display = 'none';

    } else if (viewId === 3) {
        form1.style.display = 'none';
        form2.style.display = 'none';
        form3.style.display = 'block';
        form4.style.display = 'none';
        form5.style.display = 'none';
    } else if (viewId === 4) {
        form1.style.display = 'none';
        form2.style.display = 'none';
        form3.style.display = 'none';
        form4.style.display = 'block';
        form5.style.display = 'none';

    } else if (viewId === 5) {
        form1.style.display = 'none';
        form2.style.display = 'none';
        form3.style.display = 'none';
        form4.style.display = 'none';
        form5.style.display = 'block';

    }
}

// for slider

var slider = document.querySelector(".slider");
var output = document.querySelector(".output__value");
output.innerHTML = slider.value;

slider.oninput = function () {
    output.innerHTML = this.value;


}