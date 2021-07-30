
function closeSidebar() {
    let sidebar = $('#sidebar-component');
    if (sidebar.hasClass('active')) {
        sidebar.removeClass('active');
        $('#sidebar-overlay').toggleClass('d-block');
    }
}

function openSidebar() {
    let sidebar = $('#sidebar-component');
    if (!sidebar.hasClass('active')) {
        sidebar.addClass('active');
        $('#sidebar-overlay').toggleClass('d-block');
    }
}

$(document).ready(function () {

    $(document).on("click", "#add-new-api", function () {
        let clicked = parseInt($(this).attr('data-count'));
        if (clicked === 4) {
            return;
        } else {
            $(this).attr('data-count', ++clicked);
            if (clicked === 4) {
                $(this).attr('disabled', true);
            }
        }
        let inputField = `
            <div class="col-12 mt-4" id="remove-api-${clicked}">
                <div class="row align-items-baseline">
                    <div class="col">
                        <div class="group form-group">
                            <input class="form-control" id="api-0${clicked + 1}" required type="text"/>
                            <span class="highlight"></span>
                            <span class="bar"></span>
                            <label for="api-0${clicked + 1}">API 0${clicked + 1}</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-outline-dark
                            btn-circle btn-sm btn-content-center btn-remove-api rounded-circle" data-id="remove-api-${clicked}">
                            <span class="material-icons fs-5">clear</span>
                        </button>
                    </div>
                </div>
            </div>`;

        $('#api-input-field-wrapper').append(inputField);
    });

    $(document).on('click', '.btn-remove-api', function () {
        $(this).closest("#" + $(this).attr('data-id')).remove();
        let btn_add = $('#add-new-api');
        let clicked = parseInt(btn_add.attr('data-count'));
        if (clicked > 0) {
            btn_add.attr('data-count', --clicked);
            if (clicked < 4) {
                btn_add.attr('disabled', false);
            }
        }
    });

    $(document).on('click', '#api-info', function () {
        let id = $(this).attr('data-id');
        window.location = `api-details/${id}`
    });
});

$(document).ready(function () {
    $(document).on("submit", "#apis-form", function (e) {
        e.preventDefault();

        let form = document.getElementById("apis-form")
        let obj = {};
        for (const element of form.elements) {
            if (element.type === "text") {
                console.log(element["value"])
                obj[element["id"]] = element["value"]
            }
        }
        let tokenEle = document.getElementById("csrf-token")


        $.ajax({
            url: "api_response",
            data: JSON.stringify(obj),
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            headers: {
                'X-CSRFToken': tokenEle.innerText
            },
            success: function (ajaxResponse) {
                window.location.href = "/api_response"
            },
            error: function (err){
                window.location.href = "/"
            }
        });

    });
});

//Set Page Active Link
$(document).ready(function () {
    let currentURL = window.location.pathname;
    let apiID = 0;
    let componentHeading = $('.current-component-name');
    if(currentURL.startsWith('/api-details/')) {
        apiID = currentURL.split("/api-details/")[1];
    }
    switch (currentURL) {
        case '/':
        case '/api_response':
            $('.load-page[data-href="#dashboard"]').toggleClass("active");
            if(currentURL === '/api_response') {
                componentHeading.text('Over all performance');
            } else {
                componentHeading.text('Your Test Dashboard');
            }
            break;
        case '/api-details/' + apiID:
            $('.load-page[data-href="#api-' + apiID + '"]').toggleClass("active");
            componentHeading.text('API - ' + apiID);
            break;
    }
})