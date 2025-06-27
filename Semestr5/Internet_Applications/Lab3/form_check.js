function isEmpty(someText) {
    if (typeof someText === "string" && someText.length == 0){
        return true;
    }
    return false;
  }

function isWhiteSpace(someText) {
    var ws = "\t\n\r ";
    for (var i = 0; i < someText.length; i++) {
        var c = someText.charAt(i);
        if (ws.indexOf(c) == -1) {
            return false;
        }
    }
    return true;
}

function validate(formParameter){
    isValid = true;
    if (!checkStringAndFocus(formParameter.elements["f_fname"], "Invalid name")){
        formParameter.elements["f_fname"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_fname"].classList.remove('wrong');
    }

    if (!checkString(formParameter.elements["f_lname"].value, "Invalid surname")){
        formParameter.elements["f_lname"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_lname"].classList.remove('wrong');
    }

    if(!checkEmailRegEx(formParameter.elements["f_email"].value)){
        formParameter.elements["f_email"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_email"].classList.remove('wrong');
    }

    if(!checkZIPRegEx(formParameter.elements["f_zip"].value)){
        formParameter.elements["f_zip"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_zip"].classList.remove('wrong');
    }

    if (!checkString(formParameter.elements["f_street"].value, "Invalid Street")){
        formParameter.elements["f_street"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_street"].classList.remove('wrong');
    }

    if (!checkString(formParameter.elements["f_city"].value, "Invalid City")){
        formParameter.elements["f_city"].classList.add('wrong');
        isValid = false;
    }
    else{
        formParameter.elements["f_city"].classList.remove('wrong');
    }

    alterRows(1, document.getElementsByTagName('tbody')[0])
    return isValid;
}

function checkString(stringToCheck, message){
    if (!isWhiteSpace(stringToCheck) && !isEmpty(stringToCheck)){
        return true;
    }
    return false;
}

function checkStringAndFocus(obj, msg) {
    var str = obj.value;
    var errorFieldName = "e_" + obj.name.substr(2, obj.name.length);
    if (isWhiteSpace(str) || isEmpty(str)) {
        document.getElementById(errorFieldName).innerHTML = msg;
        obj.focus();
        startTimer(errorFieldName);
        return false;
    }
    else {
        return true;
    }
}

var errorField = "";
function startTimer(fName) {
    errorField = fName;
    window.setTimeout("clearError(errorField)", 5000);
}

function clearError(objName) {
    document.getElementById(objName).innerHTML = "";
}

function showElement(e) {
    document.getElementById(e).style.visibility = 'visible';
}

function hideElement(e) {
    document.getElementById(e).style.visibility = 'hidden';
}

function checkEmailRegEx(str) {
    var email = /[a-zA-Z_0-9\.]+@[a-zA-Z_0-9\.]+\.[a-zA-Z][a-zA-Z]+/;

    if (email.test(str)){
        return true;
    }
    else {
        return false;
    }
}

function checkZIPRegEx(str) {
    var zip_template = /^[0-9]{2}[-][0-9]{3}$/;
    if (zip_template.test(str)){
        document.getElementById("zip_field").innerHTML = "OK";
        document.getElementById("zip_field").className = 'green';
        return true;
    }
    else {
        document.getElementById("zip_field").innerHTML = "WRONG";
        document.getElementById("zip_field").className = 'red';
        return false;
    }
}

function alterRows(i, e) {
    if (e) {
        if (i % 2 == 1) {
            e.setAttribute("style", "background-color: Aqua;");
        }
        e = e.nextSibling;
        while (e && e.nodeType != 1) {
            e = e.nextSibling;
        }
        alterRows(++i, e);
    }
}

function nextNode(e) {
    while (e && e.nodeType != 1) {
        e = e.nextSibling;
    }
    return e;
}

function prevNode(e) {
    while (e && e.nodeType != 1) {
        e = e.previousSibling;
    }
    return e;
}

function swapRows(b) {
    var tab = prevNode(b.previousSibling);
    var tBody = nextNode(tab.firstChild);
    var lastNode = prevNode(tBody.lastChild);
    tBody.removeChild(lastNode);
    var firstNode = nextNode(tBody.firstChild);
    tBody.insertBefore(lastNode, firstNode);
}

function cnt(form, msg, maxSize) {
    if (form.value.length > maxSize)
        form.value = form.value.substring(0, maxSize);
    else
        msg.innerHTML = maxSize - form.value.length;
}