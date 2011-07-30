grepo = window.grepo = {}

grepo.greetings =
  [ " ___ ___ ___ ___ ___ "
  , "| . |  _| -_| . | . |"
  , "|_  |_| |___|  _|___|"
  , "|___|       |_|      "
  , "                     "
  , "Search for projects in your favourite language which need *your* help!"
  , "                     "
  ].join "\n"


grepo.parse = (command) ->
  help = ->

  return unless /^grepo\s/.test command

  [_, args...] = command.split /\s+/

  # extract the language value (oh `getopt` where art thou?) and treat
  # the rest of positional arguments as keywords.
  if args[0] is "-l" or args[0] is "--language"
    language: args[1], keywords: args[2...]
  else
    # show help message.


grepo.complete = (event, term) ->
  if event.keyCode is 9   # Try to auto-complete on TAB.
    command = term.get_command();
    return no


grepo.dispatch = (command, term) ->
  options = grepo.parse command

  if not options?
    term.echo [ "Usage: grepo -l LANGUAGE [KEYWORDS]" ].join "\n"


$ ->
  $("body").terminal grepo.dispatch,
    greetings: grepo.greetings
    prompt: "$"
    exit: false
    keydown: grepo.complete
