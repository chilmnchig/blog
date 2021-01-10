$(function() {

  var game_start = false;

  $('body').keyup(function(event) {
    if (event.key === " " && game_start === false) {
      game_start = true;
      start();
    }
    if (event.key === "Escape") {
      location.reload();
    }
    return false;
  })

  const start = () => {
    var cnt = 3;
    $('.start').text(cnt);
    const cnDown = setInterval(function(){
              cnt--;
              if (cnt > 0) {
                $('.start').text(cnt);
              } else {
                clearInterval(cnDown);
                game().then(result => {
                  const [count_correct, miss, game_time] = result;
                  display_result(count_correct, miss, game_time);
                });
              }
        },1000);
  }

  async function game() {
    $('.start').hide();
    var miss = 0;
    var count_correct = 0;
    const starttime = performance.now();
    for (var i = 1; i <= 15; i++) {
      $('#' + String(i)).show();
      var roma = $('#' + String(i) + ' .roma').text();
      var output = "";
      var n = 0;
      count_correct += roma.length;
      while (n < roma.length) {
        if (roma[n] === '、') {
          roma[n] = ',';
        }
        [n, output, miss] = await typing(n, roma[n], output, miss);
        if (output) {
        $('#' + String(i) + ' .output').text(output);
        }
      }
      $('#' + String(i)).hide();
    }
    const endtime = performance.now();
    const game_time = Math.round(endtime - starttime) / 1000;
    const result = [count_correct, miss, game_time];
    return result;
  }

  function typing(n, str, output, miss) {
    return new Promise(resolve => {
      $('body').keydown(function(event) {
        $('body').off('keydown');
        if (event.key === str.toLowerCase()) {
          output += str;
          n++;
          resolve([n, output, miss]);
        } else {
          $('body').css('background-color', 'rgb(255, 195, 195)');
          setTimeout(function() {
            $('body').css('background-color', 'white');
          }, 100);
          miss++;
          resolve([n, output, miss]);
        }
      })
    })

  }

  const display_result = (count_correct, miss, game_time) => {
    $('.time span').text(String(game_time) + "秒");
    $('.miss span').text(String(miss) + "回");
    const count_total = count_correct + miss;
    $('.count span').text(String(count_total) + "字");
    const percentage = Math.round(count_correct * 10000 / count_total) / 100;
    $('.percent span').text(String(percentage) + "%");
    const wpm = count_total * 60 / game_time;
    $('.wpm span').text(String(Math.round(wpm)) + "字");
    const score = Math.round(wpm * Math.pow(percentage / 100, 3));
    $('.score span').text(String(Math.round(score)));
    $('.result').show()
  }


})
