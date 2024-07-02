// Copyright 2017 Sebastian Ouellette

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

'use strict';

function mutualGuilds(u, g, remove) {
    if (u.bot) return;
    if (!u.mutualGuilds) {
        u.mutualGuilds = new Discord.Collection();
        bot.guilds.cache.each((g) => {
            if (!g.available) return;
            let inGuild = g.members.cache.get(u.id);
            if (inGuild && !u.mutualGuilds.get(u.id)) {
                u.mutualGuilds.set(g.id, g);
            } else if (!inGuild && u.mutualGuilds.get(u.id)) {
                u.mutualGuilds.delete(g.id);
            }
        });
        return;
    }

    let mutualGuild = u.mutualGuilds.get(g.id);

    if (remove && mutualGuild) u.mutualGuilds.delete(g.id);
    else if (!remove && !mutualGuild) u.mutualGuilds.set(g.id, g);
}

function updateUsers(bunch, m = undefined, remove = false) {
    if (bunch || !m) {
        bot.users.cache.each((u) => {
            u.openDM != true && u.openDM != false
                ? (u.openDM = false)
                : undefined;
            u.mutualGuilds ? undefined : mutualGuilds(u);
            u.received ? true : false;
        });
        return;
    }

    if (m.user.openDM == undefined) m.user.openDM = false;

    if (m) mutualGuilds(m.user, m.guild, remove);
}

function updateUserDM(c, u) {
    if (c.type != Discord.ChannelType.DM || u.bot) return;
    return (u.received = selectedChan != c);
}

function dmList() {
    console.log('Switching to dms');
    // If a guild is selected then hide the guild indicator
    if (selectedGuild) {
        document.getElementById('guildIndicator').style.display = 'none';
        selectedGuild = undefined;

        // Clear guild card
        let children = document.getElementById('serverName').children;
        children[0].innerText = 'Direct Messages'; // Server name element
        if (!Array.from(children[0].classList).includes('directMsg')) {
            children[0].classList.add('directMsg'); // Toggle on the directMsg class for css
        }
        children[1].src = 'resources/icons/logo.svg'; // Server icon element
        children[2].style.display = 'none'; // Member text element
        children[3].innerText = ''; // Member count element
    }
    // Delete the selected chan variables
    selectedChan = undefined;
    selectedChatDiv = undefined;

    // Check if there are any users in the cache, if there aren't return
    if (!bot.users.cache.size) return;

    // Clear all the channels to make space for the users
    let channelList = document.getElementById('channel-elements');
    while (channelList.firstChild)
        channelList.removeChild(channelList.firstChild);

    // Clear the member bar so it can be filled with something else
    let memberList = document.getElementById('memberBar');
    memberList.innerHTML = '';

    // Clear the message list
    let messages = document.getElementById('message-list');
    while (messages.firstChild) {
        messages.removeChild(messages.firstChild);
    }

    // Categories that are going to be used to sort the users
    let categories = [
        [undefined, `Open DM's`, 'openDM'],
        [undefined, `Received DM's`, 'receivedDM'],
        [undefined, `Other DM'S`, 'otherDM'],
    ];

    // Create the categories so the users can be appended to them
    categories.forEach((c) => {
        let [element, name, id] = c;
        let category = document.createElement('div');
        category.classList.add('category');
        category.id = id;
        channelList.appendChild(category);

        // Container for the category svg and name
        let nameCategory = document.createElement('div');
        nameCategory.classList.add('categoryNameContainer');
        category.appendChild(nameCategory);

        // Create the svg icon
        let svg = document.createElement('img');
        // svg.type = "image/svg+xml";
        // svg.data
        svg.src = './resources/icons/categoryArrow.svg';
        svg.classList.add('categorySVG');
        nameCategory.appendChild(svg);

        // Create the category name
        let text = document.createElement('h5');
        text.classList.add('categoryText');
        text.innerText = name;
        nameCategory.appendChild(text);

        // Create the container for all the channels
        let div = document.createElement('div');
        div.classList.add('channelContainer');
        category.appendChild(div);

        // Event listener for opening and closing
        nameCategory.addEventListener('click', (event) => {
            category.classList.toggle('open');
        });

        categories[categories.indexOf(c)][0] = category;
    });

    // Filter the users so there aren't any bots or users that aren't in the same guild as you
    // Sort them by name
    // Note: You can't message bots with a bot account, only users
    bot.users.cache
        .filter(
            (u) => u.mutualGuilds?.size && !u.bot && (u.openDM || u.received)
        )
        .sort((u1, u2) => u1.username.localeCompare(u2.username))
        .each((u) => {
            // Get the element for the user
            let [open, received, other] = categories;

            // Create the dm channel
            let div = document.createElement('div');
            div.classList.add('dmChannel');
            div.id = u.id;

            // Create the image for the user if they have one, otherwise use discords default and animate it on hover
            let img = document.createElement('img');
            let userImg = u.displayAvatarURL({
                size: 64,
                forceStatic: true,
                extension: 'webp',
            });
            if (u.avatar?.startsWith('a_')) {
                let userGif = u.displayAvatarURL({ size: 64 });
                img.src = userGif;
                div.onmouseenter = (e) => {
                    img.src = userGif;
                };
                div.onmouseleave = (e) => {
                    img.src = userImg;
                };
            }

            // Add the class for the image and set the size
            img.classList.add('dmChannelImage');
            img.src = userImg;
            img.height = '25';
            img.width = '25';
            div.appendChild(img);

            // Add the name
            let channelName = document.createElement('h5');
            channelName.classList.add('viewableText');
            channelName.innerText = u.username;
            div.appendChild(channelName);

            // Open the dms when you click on the div
            div.addEventListener('click', (e) => {
                let previous = channelList.querySelector('.selectedChan');
                let id;
                if (previous) {
                    id = previous.id;
                    if (id != u.id) previous.classList.remove('selectedChan');
                }

                if (id != u.id) {
                    div.classList.add('selectedChan');
                    dmChannelSelect(u, div);
                }
            });

            // Check in which category the user should go in
            if (u.openDM)
                open[0].getElementsByTagName('div')[1].appendChild(div);
            else if (!u.openDM && u.received) {
                received[0].getElementsByTagName('div')[1].appendChild(div);
            } else {
                // other[0].getElementsByTagName('div')[1].appendChild(div);
            }
        });
}
