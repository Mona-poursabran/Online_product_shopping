console.log('Hello World')

var updateBtn = document.getElementsByClassName('updatecart')

for(var i=0; i< updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){

    var productId = this.dataset.product
    var action = this.dataset.action 

    console.log('productId:', productId, 'Action:', action)
    console.log('User:', user)  // it comes from base.html set there var user='{{request.user}}'
    if(user==='AnonymousUser'){
        console.log('Not Logged in!')
        alert('You have not logged in yet!')
    }else{
        updateUserOrder(productId, action)
    }
    })
    
function updateUserOrder(productId, action){
    console.log('user is logged in ')

    var url= '/updateitem/'

    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })


}
}


