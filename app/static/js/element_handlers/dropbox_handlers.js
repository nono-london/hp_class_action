
// needs to add class "dropdown-menu" in the button container
function dropbox_active_inactive(button_clicked_element){
    const dropdowns =  button_clicked_element.closest(".dropdown-menu").querySelectorAll(".dropdown-menu li a");
    //console.log(dropdowns);
    // Reset all buttons to inactive
    [... dropdowns].forEach( function (element){
      //console.log("Element");
      //console.log(element);
      element.className="dropdown-item";
    });
    //mark clicked button with active class
    button_clicked_element.className="dropdown-item active";


  }