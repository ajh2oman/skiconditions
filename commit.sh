#!/bin/sh
cd c:\Users\A.J\Documents\GitHub\skiconditions
git add --all
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
git commit -am "Regular auto-commit $(timestamp)"
git push origin master