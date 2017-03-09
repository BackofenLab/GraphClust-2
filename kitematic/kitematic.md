### Galaxy-GraphClust
## Step-by-step setup guide with Kitematic (Windows/MacOS):  ##

0. Obtain and install Kitematic from https://kitematic.com/

1. Run kitematic,  search for `graphclust` and click on `create` button
<img src="./kitematic-1.png" width="800" />

2. Wait for image to be downloaded
<img src="./kitematic-2.png" width="800" />

3. Galaxy instance starts loading, wait for message `Binding and starting galaxy control worker for main` 
<img src="./kitematic-32.png" width="800" />

4. Inside Kitematic, go to teh `settings` tab then `ports`. Configure Docker port `80` to bind on host port `8080`. Save the setting and click on binded IP for port `8080`.
<img src="./kitematic-4.png" width="800" />

5. Start browsing Galaxy html interface on `IP:8080`
<img src="./kitematic-5.png" width="800" />

