var y = "{{ typ }}";

var id = 1;
var o = { 1: "a", 2: "b", 3: "c", 4: "d" };
$("#post-form").on("submit", function (event) {
  event.preventDefault();
  var ele = document.getElementsByTagName("input");
  var t = false;
  for (i = 0; i < ele.length; i++) {
    if ((ele[i].type = "radio")) {
      if (ele[i].checked) {
        t = true;
        break;
      }
    }
  }
  if (t) {
    ele[i].checked = false;
    $.ajax({
      url: "{% url 'check_quiz' %}",
      type: "POST",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}",
        ans: ele[i].id,
        id: id,
        ty: y,
      },
      success: function (json) {
        if (Object.keys(json).length !== 0) {
          id += 1;
          console.log(json, id, json.id);
          var chh = json.choose.split(",");
          var el = document.getElementById("gg");
          document.getElementById("question").innerText =
            json.id + ". " + json.question;
          document.getElementById("kl").innerText = json.id + "/" + "{{ len }}";
          for (i = 0; i < chh.length; i++) {
            el.innerHTML += `    <li>
                {" "}
                <input class="answer" id="${o[i]}" name="answer" type="radio" />
                <label for="a" id="a_text">
                  "${chh[i]}"
                </label>
              </li>`;
          }
        } else {
          window.location.href = "/result";
        }
      },
    });
  }
  document.querySelector("[name=csrfmiddlewaretoken]").type = "hidden";
});

window.addEventListener("load", function () {
  alert(123);
  var q = "{{ question }}";
  var chh = " {{ ch }}".split(",");
  var id = "{{ id }}";

  var el = document.getElementById("gg");
  document.getElementById("question").innerText = id + ". " + q;
  for (i = 0; i < chh.length; i++) {
    el.innerHTML += ` <li>
        <input class="answer" id="${o[i]}" name="answer" type="radio" />
        <label for="a" id="a_text">
          "${chh[i]}"
        </label>
      </li>
    `;
  }
});
