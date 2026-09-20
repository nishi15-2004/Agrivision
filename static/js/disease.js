// ==========================================
// AgriMitra Disease Detection JavaScript
// ==========================================


// ==========================================
// Image Preview Before Upload
// ==========================================

const imageInput = document.getElementById("leafImage");


if(imageInput){


    imageInput.addEventListener("change", function(){


        const file = this.files[0];


        if(file){


            const reader = new FileReader();


            reader.onload = function(e){


                let preview = document.querySelector(".preview-image");


                if(!preview){


                    preview = document.createElement("img");

                    preview.className = "preview-image";


                    document.querySelector(".upload-card")
                    .appendChild(preview);


                }


                preview.src = e.target.result;


            }


            reader.readAsDataURL(file);


        }


    });


}



// ==========================================
// Upload Button Animation
// ==========================================


const detectButton =
document.querySelector(".upload-card button");



if(detectButton){


    detectButton.addEventListener("click", function(){


        this.innerHTML = "🔍 Detecting...";


        this.style.opacity = "0.8";


    });


}




// ==========================================
// Result Card Animation
// ==========================================


window.addEventListener("load", function(){


    const result =
    document.querySelector(".result-card");



    if(result){


        result.style.opacity="0";


        result.style.transform=
        "translateY(30px)";



        setTimeout(()=>{


            result.style.transition=
            "0.6s ease";


            result.style.opacity="1";


            result.style.transform=
            "translateY(0)";



        },200);



    }


});




// ==========================================
// Tips Card Animation
// ==========================================


const tipCards =
document.querySelectorAll(".tip-card");



tipCards.forEach((card,index)=>{


    card.style.opacity="0";


    setTimeout(()=>{


        card.style.transition=
        "0.5s ease";


        card.style.opacity="1";


    },index*150);



});