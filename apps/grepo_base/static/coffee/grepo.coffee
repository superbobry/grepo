grepo = window.grepo ||= {}

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


grepo.match = (language) ->
  if language is ""
    grepo.LANGUAGES[0]
  else
    regex = new RegExp("^#{language}")
    for candidate in grepo.LANGUAGES
      return candidate if regex.test candidate

    language


grepo.complete = (event, term) ->
  if event.keyCode is 9   # Try to auto-complete on TAB.
    options = grepo.parse term.get_command()

    if options? and options.language?
      # a) auto-complete language
      if not options.keywords.length
        term.set_command "grepo -l #{grepo.match options.language} "
      else
        # query the server for the closest matching tag.

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
