import re
import os
import sys
import libmathcat

if (len(sys.argv) != 2):
  raise Exception("no argument")

htmlfile=sys.argv[1]


def SetMathCATPreferences():
  try:
    libmathcat.SetRulesDir(
      # this assumes the Rules dir is in the same dir a the library. Modify as needed
      os.path.join( os.path.dirname(os.path.abspath(__file__)), "Rules")
    )
  except Exception as e:
    print("problem with finding the MathCAT rules")

  try:
    libmathcat.SetPreference("TTS", "none")
    libmathcat.SetPreference("Language", "en")         # Also "id" and "vi"
    libmathcat.SetPreference("SpeechStyle", "SimpleSpeak")   # Also "ClearSpeak"
    libmathcat.SetPreference("Verbosity", "Verbose")   # also terse "Terse"/"Medium"
    libmathcat.SetPreference("CapitalLetters_UseWord", "false")   # if "true", X => "cap x"
  except Exception as e:
      print("problem with setting a preference")

def SetMathMLForMathCAT(mathml: str):
    libmathcat.SetMathML(mathml)


def GetSpeech():
  try:
    return libmathcat.GetSpokenText()
  except Exception as e:
    return "problem with getting speech for MathML"



SetMathCATPreferences()   # you only need to this once


htmlstr = open(htmlfile,'r',encoding="utf-8").read()


mmls=re.split(r'(<math .*?</math>)', htmlstr, flags=re.DOTALL)

sys.stdout.reconfigure(encoding='utf-8')

i=0
for mml in mmls:
    print (mml,end="")
    i=i+1
    if(i % 2 == 0):
        try:
            SetMathMLForMathCAT(mml)
            print ("\n    <div class=\"mathcat\">{}</div>".format(GetSpeech() ))
        except:
            print ("\n    <div class=\"mathcat\">problem with SetMathML</div>")

