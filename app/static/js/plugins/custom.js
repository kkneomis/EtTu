/* ====== Index ======

1. JEKYLL INSTANT SEARCH
2. SCROLLBAR CONTENT
3. TOOLTIPS AND POPOVER
4. JVECTORMAP DASHBOARD
5. JVECTORMAP ANALYTICS
6. JVECTORMAP WIDGET
7. MULTIPLE SELECT
8. LOADING BUTTON
  8.1. BIND NORMAL BUTTONS
  8.2. BIND PROGRESS BUTTONS AND SIMULATE LOADING PROGRESS
9. TOASTER
10. PROGRESS BAR

====== End ======*/

$(document).ready(function() {
  "use strict";

  /*======== 2. SCROLLBAR CONTENT ========*/

  function scrollWithBigMedia(media) {
    var $elDataScrollHeight = $("[data-scroll-height]");
    if (media.matches) {
      /* The viewport is greater than, or equal to media screen size */
      $elDataScrollHeight.each(function() {
        var scrollHeight = $(this).attr("data-scroll-height");
        $(this).css({ height: scrollHeight + "px", overflow: "hidden" });
      });

      //For content that needs scroll
      $(".slim-scroll")
        .slimScroll({
          opacity: 0,
          height: "100%",
          color: "#999",
          size: "5px",
          wheelStep: 10
        })
        .mouseover(function() {
          $(this)
            .next(".slimScrollBar")
            .css("opacity", 0.4);
        });
    } else {
      /* The viewport is less than media screen size */
      $elDataScrollHeight.css({ height: "auto", overflow: "auto" });
    }
  }

  var media = window.matchMedia("(min-width: 992px)");
  scrollWithBigMedia(media); // Call listener function at run time
  media.addListener(scrollWithBigMedia); // Attach listener function on state changes

  /*======== 3. TOOLTIPS AND POPOVER ========*/
  $('[data-toggle="tooltip"]').tooltip({
    container: "body",
    template:
      '<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
  });
  $('[data-toggle="popover"]').popover();


  /*======== 5. JVECTORMAP ANALYTICS ========*/
  var mapData2 = {
    IN: 19000,
    US: 13000,
    TR: 9500,
    DO: 7500,
    PL: 4600,
    UK: 4000
  };

  if (document.getElementById("analytic-world")) {
    $("#analytic-world").vectorMap({
      map: "world_mill",
      backgroundColor: "transparent",
      zoomOnScroll: false,
      regionStyle: {
        initial: {
          fill: "#e4e4e4",
          "fill-opacity": 0.9,
          stroke: "none",
          "stroke-width": 0,
          "stroke-opacity": 0
        }
      },

      series: {
        regions: [
          {
            values: mapData2,
            scale: ["#6a9ef9", "#b6d0ff"],
            normalizeFunction: "polynomial"
          }
        ]
      }
    });
  }





  /*======== 9. TOASTER ========*/
  function callToaster(positionClass) {
    if (document.getElementById("toaster")) {
      toastr.options = {
        closeButton: true,
        debug: false,
        newestOnTop: false,
        progressBar: true,
        positionClass: positionClass,
        preventDuplicates: false,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "5000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
      };
      toastr.success("Welcome to sleek", "Howdy!");
    }
  }

  if (document.dir != "rtl" ){
    callToaster("toast-top-right");
  }else {
    callToaster("toast-top-left");
  }

  /*======== 10. PROGRESS BAR ========*/
  NProgress.done();
});
