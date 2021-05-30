// Validating Empty Field
function check_empty() {
if (document.getElementById('name').value == "" || document.getElementById('email').value == "") {
alert("Fill All Fields !");
} else {
document.getElementById('form').submit();
alert("Form Submitted Successfully...");
}
}
//Function To Display Popup
function div_show() {
document.getElementById('btn_white_product-sheet').style.display = "block";
}
//Function to Hide Popup
function div_hide(){
document.getElementById('btn_white_product-sheet').style.display = "none";
}