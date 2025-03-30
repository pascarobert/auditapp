//Test
console.log("test");

//Image Slider
var counter = 1;
    setInterval(function(){
      document.getElementById('radio' + counter).checked = true;
      counter++;
      if(counter > 4){
        counter = 1;
      }
    }, 5000);

//Information
const buttons = document.querySelectorAll('button');
buttons.forEach( button =>{
    button.addEventListener('click',()=>{
        const faq = button.nextElementSibling;
        const icon = button.children[1];

        faq.classList.toggle('show');
        icon.classList.toggle('rotate');
    })
} )


//Eroare neincarcare document

document.addEventListener("DOMContentLoaded", function() {
  var form = document.querySelector('form');

  form.addEventListener('submit', function(event) {
      var financialSuite = document.getElementById('financial_suite');
      var portofolio = document.getElementById('portofolio');
      var materialitate = document.getElementById('materialitate');
      var confirmariBancare = document.getElementById('confirmari_bancare');

      if (!financialSuite.files.length || !portofolio.files.length || !materialitate.files.length || !confirmariBancare.files.length) {
          event.preventDefault(); // Previne trimiterea formularului

          // Afișează un mesaj de avertizare
          alert('Te rog să încarci toate documentele necesare!');
      }
  });
});