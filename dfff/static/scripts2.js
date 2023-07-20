let obj = document.querySelectorAll('.yoma')

obj.forEach((itemed) => 
{   
    let item = itemed.querySelector('button');
    
    item.addEventListener('click', () => 
        {   
            let butttons = document.querySelectorAll('button');
            butttons.forEach((items) => 
            {
                if(items.textContent == "Copied !")
                items.textContent = "Copy Link !";
            });

            navigator.clipboard.writeText(itemed.querySelector(".ohmy").textContent)
            item.textContent = "Copied !"
        })
});