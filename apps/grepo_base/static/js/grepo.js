$(function() {
  var greetings = [ " ___ ___ ___ ___ ___ "
                  , "| . |  _| -_| . | . |"
                  , "|_  |_| |___|  _|___|"
                  , "|___|       |_|      "
                  , "                     "
                  ];

  $("body").terminal(function(command, term) {
    // handle input here ...
  }, {
    greetings: greetings.join("\n")
  , prompt: "$"
  });
});
