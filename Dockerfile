FROM python:3.12

WORKDIR /workdir

# install zandronum (and dependencies)
RUN echo "deb http://debian.drdteam.org/ stable multiverse" > /etc/apt/sources.list.d/drdteam.list \
 && wget -O - http://debian.drdteam.org/drdteam.gpg | apt-key add - \
 && apt-get update \
 && apt-get install -y zandronum

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy the rest of the source code
COPY . .

# Copy WAD files from host machine into the container
# ~/.config/zandronum is a default directory for zandronum WAD files
COPY wads/DOOM2.WAD /root/.config/zandronum/DOOM2.WAD
COPY wads/back-to-saturn-x.pk3 /root/.config/zandronum/back-to-saturn-x.pk3
COPY wads/1000-lines-3.wad /root/.config/zandronum/1000-lines-3.wad

EXPOSE 5000 10666 10667  10668 10669 10670
CMD ["python", "run.py"]
