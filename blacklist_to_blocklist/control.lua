function create_allowlist_function()
	commands.add_command("allowlist", {"command-help.allowlist"}, function()
		game.print({"allowlist.reminder"})
	end)
end

script.on_init(create_allowlist_function)
script.on_load(create_allowlist_function)
