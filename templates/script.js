<script>
function showTwitter() {
  // Get the checkbox
  var checkBox = document.getElementById('twitter_check');
  // Get the output text
  var text = document.getElementById("text_twitter");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true) {
    text.style.display = "block";
  } else {
    text.style.display = "none";
  }
}

function showNews() {
  // Get the checkbox
  var checkBox = document.getElementById('news_check');
  // Get the output text
  var text = document.getElementById("text_news");
  var form = document.getElementById("formNews");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true) {
    text.style.display = "block";
    form.style.display = "block";
  } else {
    text.style.display = "none";
    form.style.display = "none";
  }
}
</script>
