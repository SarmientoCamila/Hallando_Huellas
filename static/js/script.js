loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  // Aquí la lógica para verificar los datos del login
let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.toggle('active');
    searchForm.classList.remove('active');
    cartItem.classList.remove('active');
}

let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active');
    navbar.classList.remove('active');
    cartItem.classList.remove('active');
}

let cartItem = document.querySelector('.cart-items-container');

document.querySelector('#cart-btn').onclick = () =>{
    cartItem.classList.toggle('active');
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
}

window.onscroll = () =>{
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
    cartItem.classList.remove('active');
}
const loginForm = document.querySelector('form.vertical-form');
const misMascotasBtn = document.getElementById('mis-mascotas-btn');


  // Si los datos son correctos, muestra el botón "Mis mascotas"
  misMascotasBtn.style.display = 'block';
  // Oculta el formulario de login
  loginForm.style.display = 'none';
});
