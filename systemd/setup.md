Copy the `systemd` into correct spot

```
sudo cp ~/hueComposer/systemd/hueComposer.service /etc/systemd/system
```

then enable it

```
sudo systemctl daemon-reload
sudo systemctl enable hueComposer
```

Now the code will attempt to start at boot.
