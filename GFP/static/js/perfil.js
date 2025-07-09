 var swiper = new Swiper(".mySwiper", {
    navigation:{
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    spaceBetween: 10,
    slidesPerView: 1,
    loop: true,
});

function abrirModal(id) {
            let modal = document.getElementById("modal-" + id);
            modal.classList.add("show");
            modal.style.display = "block";
        }

        function fecharModal(id) {
            let modal = document.getElementById("modal-" + id);
            modal.classList.remove("show");
            modal.style.display = "none";
        }

        var swiper = new Swiper(".mySwiper", {
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            spaceBetween: 10,
            slidesPerView: 1,
            loop: true,
            on: {
                slideChange: function () {

                    document.querySelectorAll(".modal").forEach(function(modal){
                        modal.classList.remove("show");
                        modal.style.display = "none";
                    });

                }
            }
        });

        function apagarBoleto(){
            document.getElementById('action_type').value = 'delete';

            document.getElementById("form-{{ img.id }}").submit();

        }

        document.getElementById("form-{{ img.id }}").addEventListener("submit", function(event){

        })