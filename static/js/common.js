function checkMandatoryField(cls_name)
    {
    //item_required1
        var emptyFlag = 0;
        var firstError = 0;

        $('.'+cls_name).filter(function () {
            if(this.id)
            {
                if(this.value == '')
                {
                    emptyFlag = 1;
                    $('#'+this.id).addClass('redborder');

                    if(firstError == 0)
                    {
                        $('#'+this.id).focus();
                        firstError=1;
                    }

                    if($('#'+this.id).hasClass('selectpicker'))
                    {
                        $('#'+this.id).selectpicker('refresh');
                    }
                }
                else{
                    if($('#'+this.id).hasClass('redborder'))
                    {
                        $('#'+this.id).removeClass('redborder');
                    }
                    if($('#'+this.id).hasClass('selectpicker'))
                    {
                        $("#"+this.id).closest("div").removeClass("redborder");
                        $('#'+this.id).selectpicker('refresh');
                    }
                }
            }
        });
        return emptyFlag;
    }


$(document).on('keyup', '.item_required', function(){
    requiredField($(this).attr('id'))
});


$(document).on('change', '.item_required', function(){
    requiredField($(this).attr('id'))
});


function requiredField(id)
{
    var value = $('#'+id).val();

    if(!value)
    {
        $('#'+id).addClass("redborder");
        $('#'+id).focus();
    }
    else{
        $('#'+id).removeClass("redborder");
        if($('#'+id).hasClass("selectpicker"))
        {
            $("#"+id).closest("div").removeClass("redborder");
        }

        if($('#'+id).hasClass( "email" ))
        {
            var user_email_id = $('#'+id).val();
            if(isValidEmail(user_email_id))
            {
                if($('#'+id).hasClass("redborder"))
                {
                    $('#'+id).removeClass('redborder');
                }
            }
            else{
                $('#'+id).addClass('redborder');
                $('#'+id).focus();
            }
        }
    }

    if($('#'+id).hasClass("selectpicker"))
    {
        $('#'+id).selectpicker('refresh');
    }
}