import sublime, sublime_plugin, os, subprocess
PLUGIN_DIR = os.path.abspath(os.path.dirname(__file__))

class ProcessDataBagItemCommand(sublime_plugin.TextCommand):
    def str(self, s):
        try:
            # Python 2
            return unicode(s, "utf_8")
        except NameError:
            # Python 3
            return str(s, "utf_8")

    def run(self, edit):
        repository_root = self.view.window().folders()[0]
        secret_file = os.path.join(repository_root, "data_bag_key")

        # Read data_bag_key
        if not os.path.exists(secret_file):
          sublime.error_message("data_bag_key not found:\n%s" % secret_file)
          return
        with open(secret_file) as f:
          secret = f.read()

        # Get content
        region_all = sublime.Region(0, self.view.size())
        data = self.view.substr(region_all)

        # Encrypt / Decrypt
        processed_data = self.process(data, secret)
        self.view.replace(edit, region_all, processed_data)

    def process(self, data, secret):
        raise "Please override #process"

    def run_script(self, script_name, data, secret):
        settings = sublime.load_settings("ChefEncryptedDataBag.sublime-settings")
        ruby = settings.get("ruby", "ruby")

        script_path = os.path.join(PLUGIN_DIR, script_name)
        cmd = [ruby, "--encoding", "utf-8", script_path, secret]

        proc = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdout, stderr = proc.communicate(data.encode("utf_8"))

        returncode = proc.wait()
        if returncode != 0:
            sublime.error_message(self.str(stderr))
            raise
        return self.str(stdout)

class EncryptDataBagItemCommand(ProcessDataBagItemCommand):
    def process(self, data, secret):
        return self.run_script("chef_encrypt_databag_item.rb", data, secret)

class DecryptDataBagItemCommand(ProcessDataBagItemCommand):
    def process(self, data, secret):
        return self.run_script("chef_decrypt_databag_item.rb", data, secret)
