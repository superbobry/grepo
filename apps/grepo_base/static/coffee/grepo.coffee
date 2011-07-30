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
  [name, argv...] = command.split(/\s+/)

  if name isnt "grepo"
    term.error "command not found: #{name}"
  else
    $.getJSON "/opster/", argv: argv, (xhr) ->
      term.error(xhr.stderr) if xhr.stderr
      term.echo (xhr.stdout) if xhr.stdout


$ ->
  $("body").terminal grepo.dispatch,
    greetings: grepo.greetings
    prompt: "$"
    exit: false
    keydown: grepo.complete
