grepo = window.grepo ||= {}

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
      when "-o"
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
    term.error "command not found: #{name}" if name
  else
    $.getJSON "/opster/", argv: argv, (xhr) ->
      return term.error(xhr.stderr) if xhr.stderr
      return term.echo (xhr.stdout) if xhr.stdout

      $.getJSON "/search/", xhr.options, (xhr) ->
        repositories = xhr.repositories

        if not repositories.length
          term.echo "We got nothing for you at the moment <_<"
        else
          term.echo xhr.repositories.join("\n\n")


$ ->
  grepo.el = $("#grepo").terminal grepo.dispatch,
    greetings: no
    prompt: "$"
    name: "grepo"
    exit: false
    keydown: grepo.complete

  grepo.el.mousewheel (event, delta) ->
    $(if delta > 0 then "#up" else "#down").click()

  $("#down").click -> grepo.el.scroll(  12 * 5 )
  $("#up").click   -> grepo.el.scroll(-(12 * 5))

  grepo.el.echo "  grepo -l LANGUAGE [-o] RESULTS [KEYWORDS]"
  grepo.el.echo " "
  grepo.el.echo "  grepo helps you find open-source projects to contribute to."
  grepo.el.echo " "
  grepo.el.echo "  Simply specify the programming language and grepo will output"
  grepo.el.echo "  a list projects that need your help most."
  grepo.el.echo " "
  grepo.el.echo "  options:"
  grepo.el.echo " "
  grepo.el.echo "  -l --language  programming language you want to grepo for"
  grepo.el.echo "  -o --only      maximum number of projects to look up (default: 20)"
  grepo.el.echo "  -h --help      show help"
  grepo.el.echo " "
