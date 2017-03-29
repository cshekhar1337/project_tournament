# project_tournament
## Steps for installation 
1. Go to the desired folder where you want to copy this project
2. Execute this command on the termnal "https://github.com/cshekhar1337/project_tournament.git"
3. Install vagrant on your pc and execute cd project_tournament on terminal ..  
4. Now execute "vagrant up --provision"
5. execute "vagrant ssh" to connect to the ubuntu vm
6. cd vagrant/tournament
7. Type "psql" on terminal and press enter
8. Execute "\i tournament.sql"  -> this creates database, tables, trigger and functions
9. \q to exit psql command line
10. Execute "python tournament_test.py"
