function showAlert(){
    var username=document.getElementById('username').value;
    var password=document.getElementById('password').value;
    var cpassword=document.getElementById('cpassword').value;

    if (!username || !password || !cpassword ){
        alert('please fill out the rquired field.');
    }

    alert('Registration Successful,Now you can log in ');
}