document
  .getElementById("accept-button")
  .addEventListener("click", function (event) {
    // check that disclaimer scroll has been scrolled to the bottom
    let disclaimerScroll = document.getElementById("disclaimer-scroll");
    if (
      disclaimerScroll.scrollTop + disclaimerScroll.clientHeight !==
      disclaimerScroll.scrollHeight
    ) {
      alert(
        "Please scroll to the bottom before accepting to ensure you have read the entire contents.",
      );
      return;
    }

    console.log("accept-button clicked");
    window.location.href = "login.html";
  });
