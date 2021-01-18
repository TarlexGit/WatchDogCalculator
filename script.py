import os
import csv 
import argparse


class WatchDogCalculator:
    def __init__(self, folder_name, ticker):
        self.folder_name = folder_name 
        self.ticker = ticker  

    def watch(self):  
        csv_files = [os.path.join(root, name)
                        for root, dirs, files in os.walk(self.folder_name)
                            for name in files
                                if name.endswith((".csv"))] 
        return csv_files 
    
    def read_csv(self, path_to_file): 
        f = open(path_to_file, 'r')  
        stack = []
        with f:  
            reader = csv.DictReader(f) 
            for row in reader: 
                if row['Name']==self.ticker: 
                    stack.append(row)  
                else: pass
            yield stack

    def average(self):
        files = self.watch() 
        
        try: 
            for f in files:   
                open_stack = [] 
                high_stack = []
                low_stack = []
                close_stack = []
                ticker_data = self.read_csv(f)
                
                n = next(ticker_data)
                
                for data in n:
                    open_stack.append( "%.3f" % float(data["open"]) )
                    high_stack.append("%.3f" % float(data["high"]))
                    low_stack.append("%.3f" % float(data["low"]))
                    close_stack.append("%.3f" % float(data["close"]))
                    

                out_data = {"open":  f"%.3f" % (sum([float(x)  for x in open_stack])/len(open_stack)), 
                            "high":f"%.3f" % (sum([float(x)  for x in high_stack])/len(high_stack)),
                            "low":f"%.3f" % (sum([float(x)  for x in low_stack])/len(low_stack)), 
                            "close":f"%.3f" % (sum([float(x)  for x in close_stack])/len(close_stack))} 
                print(out_data)
        except: pass
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parse ticker in files')
    parser.add_argument('folder_name', type=str, help='folder_name')
    parser.add_argument('ticker', type=str, help='ticker')
    args = parser.parse_args()

    WatchDogCalculator(args.folder_name, args.ticker).average()
     