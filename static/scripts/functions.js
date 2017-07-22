function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.body.style.backgroundColor = "white";
}
function fill(str,id1,id2){
    var kbd=document.getElementById(id1)
    var text=document.getElementById(id2)
    if(!text.value.includes(str))
    {
        kbd.style.backgroundColor="Green"
        kbd.style.color="white"
        text.value=text.value+str+","
    }
    else
    {
        console.log("reached")
        kbd.style.backgroundColor="Black"
        kbd.style.color="white"
        text.value=text.value.replace(str+",","")
    }
}
$(function(){
    $(".flip").flip({
        trigger: 'hover'
    });
});
