function bidFormHandler() {
       // document.forms return an HTML collection object of all forms on the page
    // You can access each form using its names and each input tags name in each form and their value
    // x = document.forms['myForm']['fname'].value;

    bid = parseFloat(document.forms['placeBidForm']['bid'].value)

    const highest = parseFloat(JSON.parse(document.getElementById('higher-bidder-data').textContent).price) ;
    const bidMsg = document.getElementById("bid-msg")

    if (bid <= highest) {
        bidMsg.style.color = "red";
        bidMsg.style.fontWeight = "bold"
        return false;
    }
}