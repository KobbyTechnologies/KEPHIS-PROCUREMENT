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