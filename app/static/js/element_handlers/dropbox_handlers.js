
// needs to add class "dropdown-menu" in the button container
function dropbox_active_inactive(button_clicked_element, text_prefix){
    const dropdown_nodes =  button_clicked_element.closest(".dropdown-menu").querySelectorAll(".dropdown-menu li a");
    const dropdown_container = button_clicked_element.closest(".button-active-handler").querySelector(".dropdown-toggle");
    //console.log(dropdowns);
    // Reset all buttons to inactive
    [... dropdowns].forEach( function (element){
      //console.log("Element");
      //console.log(element);
      element.className="dropdown-item";
    });
    // mark clicked button with active class
    button_clicked_element.className="dropdown-item active";
    // update main text container
    dropdown_container.innerHTML =`${text_prefix}: ${button_clicked_element.innerHTML }`;


  }