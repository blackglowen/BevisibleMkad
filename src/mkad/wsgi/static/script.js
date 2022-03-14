var btn = document.getElementById('mkad-btn');
btn.addEventListener('click', function(){
    var addr = window.prompt("Enter an address:");
    if(addr){
      window.location.href = "/mkad/api/" + addr;
    }
})
