grepo = window.grepo = {}

# Parse a given array of command line arguments and return it as
# an `Object`.
grepo.parse = (command) ->
  return unless /^grepo\s/.test command

  [_, args...] = args.split /\s+/

  for arg in args
    return help: true if arg is "-h" or arg is "--help"

grepo.greeting = (fn) ->
  fn [ " ___ ___ ___ ___ ___ "
     , "| . |  _| -_| . | . |"
     , "|_  |_| |___|  _|___|"
     , "|___|       |_|      "
     , "                     "
     ].join "\n"


grepo.complete = (event, term) ->
  if event.keyCode is 9   # Try to auto-complete on TAB.
    command = term.get_command();
    return no


$ ->
  $("body").terminal ((command, term) ->
    options = grepo.parse command
  ), greetings: greetings.join("\n"), prompt: "$", exit: false, keydown: grepo.complete
