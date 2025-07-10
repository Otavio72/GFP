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

        var swiper = new Swiper(".Swiper_perfil", {
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
