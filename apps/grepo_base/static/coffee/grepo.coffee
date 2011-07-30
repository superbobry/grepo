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
    command = term.get_command()
    [command..., key, value] = command.split /\s+/

    if key[0] isnt "-"
      command.push key

      # seems like we have a -fBAR case.
      if value[0] is "-"
        [key, value] = [value.substring(0, 2), value.substring(2)]
      # okay, complete keyword
      else
        # query the server for the closest matching tag.
        return

    # complete an argument.
    switch key
      when "-n"
        value = parseInt(value or "10", 10) * 2
      when "-l"
        value = grepo.match(value)

    command.push key
    command.push value
    term.set_command command.join(" ")

    return no


grepo.dispatch = (command, term) ->
  [name, argv...] = command.split(/\s+/)

  if name isnt "grepo"
    term.error "command not found: #{name}"
  else
    $.getJSON "/opster/", argv: argv, (xhr) ->
      return term.error(xhr.stderr) if xhr.stderr
      return term.echo (xhr.stdout) if xhr.stdout

      $.getJSON "/query/", xhr.options, (xhr) ->
        # render results.


$ ->
  $("body").terminal grepo.dispatch,
    greetings: grepo.greetings
    prompt: "$"
    exit: false
    keydown: grepo.complete
