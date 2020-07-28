//used to set placeholder values in the registration form

//using vanilla javascript we query all fields

    var form_fields = document.getElementsByTagName('input')
        form_fields[1].placeholder = 'Username';
        form_fields[2].placeholder = 'Email';
        form_fields[3].placeholder = 'Enter Password';
        form_fields[4].placeholder = 'Re-enter Password';

        for(var fields in form_fields){
            form_fields[fields].className += ' form-control';
        }