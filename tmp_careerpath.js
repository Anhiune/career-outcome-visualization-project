jQuery(document).ready(function(){
    // Set up tabs
    var panelWidth = jQuery('.panel').width();
    var tabCount = jQuery('.tab').length;
    var panelContainerWidth = panelWidth * tabCount;

    jQuery('.panel-container').width(panelContainerWidth);

    //set the default location (fix ie 6 issue)
    jQuery('.tabs').append('<div class="lava" />');
    jQuery('.lava').css({width:jQuery('span.tab:first').outerWidth(),left:jQuery('span.tab:first').position()['left']});

    jQuery('.tab').each(function(i){
        jQuery(this).click(function () {

            //scroll the lava to current item position
            jQuery('.lava').stop().animate({width:jQuery(this).outerWidth(),left:jQuery(this).position()['left']}, {duration:200});

            //scroll the panel to the correct content
            jQuery('.panel-container').stop().animate({left:jQuery('.panel').eq(i).position()['left'] * (-1)}, {duration:200});
        });
    });

    // Data slider
    var fiveYearImgsCount = jQuery('#panel-2').find('.tinypics img').length;

    jQuery('#5-year-slider')
    //.after('<span id="slider-output" />')
    .simpleSlider({range:[1,fiveYearImgsCount],step:'1',snap:true,highlight:true})
    .bind("slider:ready slider:changed", function (event, data) {
        /*$(this)
        .nextAll("#slider-output")
        .html(data.value);*/
        context = getContext(jQuery(this));
        newSrc = context.find('.tinypics img').eq(data.value - 1).attr('src');
        newAlt = context.find('.tinypics img').eq(data.value - 1).attr('alt');
        switchImage(newSrc, newAlt, context);
    });

    // Store bigpic src and alt for later, set up timer to temporarily
    // disable hover events;
    var bigpicSrc, bigpicAlt, hoverStatesTimer;
    // Set bigpic to Composite image (all majors)
    setBigPicSrc();
    // Switch and restore images on hover
    hoverStates();
    // Change image on click and temporarily disable hover
    clickStates();

    function clickStates(){
        jQuery('map area, .tinypics img').click(function(e){
            context = getContext(jQuery(this));
            jQuery('.tinypics img', context).off('hover');
            newSrc = jQuery(this).attr('href');
            if(newSrc == undefined) newSrc = jQuery(this).attr('src');
            newAlt = jQuery(this).attr('alt');
            switchImage(newSrc, newAlt, context);
            // Make bigpic src 'sticky'
            setBigPicSrc();
            setHoverStatesTimer();
            e.preventDefault();
        });
    }

    function hoverStates(){
        var context;
        jQuery('map area, .tinypics img').hover(
        function(){
            newSrc = jQuery(this).attr('href');
            if(newSrc == undefined) newSrc = jQuery(this).attr('src');
            newAlt = jQuery(this).attr('alt');
            context = getContext(jQuery(this));
            switchImage(newSrc, newAlt, context);
        },
        function(){
            switchImageBack(context);
        }
        );
    }

    function getContext(el){
        return el.parents('.panel');
    }
    function switchImage(newSrc, newAlt, context){
        jQuery('.bigpic img', context).attr('src',newSrc).attr('alt',newAlt);
        jQuery('.bigpic h2', context).text(newAlt);
    }
    function switchImageBack(context){
        jQuery('.bigpic img', context).attr('src',bigpicSrc).attr('alt',bigpicAlt);
        jQuery('.bigpic h2', context).text(bigpicAlt);
    }
    function setBigPicSrc(){
        bigpicSrc = jQuery('#bigpic img').attr('src');
        bigpicAlt = jQuery('#bigpic img').attr('alt');
    }
    function setHoverStatesTimer(){
        if(hoverStatesTimer) {
            clearTimeout(hoverStatesTimer);
            hoverStatesTimer = null;
        }
        hoverStatesTimer = setTimeout(function(){
            hoverStates();
        }, 2000);
    }
});
