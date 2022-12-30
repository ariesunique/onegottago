# One Gotta Go

This is a simple game that I used to play with my family. The idea is to provide a list of 4 related items. The other players must decide which of the 4 they would get rid of (ie, which one could they live without it).

This repo provides an online version of that game.

These are two separate services that can be developed and deployed independently. 

The UI is written in Flask and Bootstrap.

The API is a REST API written using FlaskAPI. It reads and writes to Cloud DataStore in GCP. Both the API and UI can be deployed to CloudRun. 

Installation, development, and deployment instructions are within each subdirs.