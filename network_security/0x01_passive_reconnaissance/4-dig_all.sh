#!/bin/bash
^dig(?=.*\+noall.\+answer)(?=.*any)(?=.*\$1)(?:\s+(?:any|\+noall.\+answer|\$1))+$ 
