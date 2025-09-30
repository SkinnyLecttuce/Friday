class Syncer():
    def __init__(self):
        self.input_file = 'current_data/current_input.txt'
        self.output_file = 'current_data/current_output.txt'

    def sync_read_input(self):
        f = open(self.input_file, 'r')
        fr = f.readlines()
        fr = fr[0].split('\n')
        fr = fr[0]
        f.close()
        return fr

    def sync_read_output(self):
        f = open(self.output_file, 'r')
        fr = f.readlines()
        fr = fr[0].split('\n')
        fr = fr[0]
        f.close()
        return fr

    def sync_input(self,current_input):
        f = open(self.input_file,'w')
        f.write(str(current_input))
        f.close()

    def sync_output(self,current_output):
        f = open(self.output_file,'w')
        f.write(str(current_output))
        f.close()

    def sync_files(self,current_input,current_output):
        self.input_file(str(current_input))
        self.output_file(str(current_output))

    def sync_refresh(self):
        f = open(self.input_file,'w')
        f.write('')
        f.close()

        f = open(self.output_file,'w')
        f.write('')
        f.close()