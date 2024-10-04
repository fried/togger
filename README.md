# togger 

T-String Logging Library built ontop of python logging module. 

Logger names are always based on the `__NAME__`

Strings formatting is lazy, so if the log level is not enabled, no stringification takes place. 

```python
# Works with all the standard levels
from togger import debug, fatal

debug"fun times"
fatal"oh noes"

# Works with logging by level int instead of name
from togger import log

level1=log(1)
level1"{level1!r} Error Message"

# Works with custom level names
import logging
logging.addLevelName(51, "SPEW")
from togger import spew

spew"halp! i'm dying here"
```

