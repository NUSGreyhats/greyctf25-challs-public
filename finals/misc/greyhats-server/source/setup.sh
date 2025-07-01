#!/bin/bash

FLAG="grey{wh0_kn3w_y0u_c4n_u5e_o4uth_f0r_ssh?!?_atFj5QNm3xgpctX8}"
OIDC_CLIENT_ID="<GOOGLE_OAUTH_CLIENT_ID>"
OIDC_CLIENT_SECRET="<GOOGLE_OAUTH_CLIENT_SECRET>"

apt-get update
wget https://launchpad.net/~ubuntu-enterprise-desktop/+archive/ubuntu/authd/+build/30928428/+files/authd_0.5.3-0ubuntu24.04.1_amd64.deb
dpkg -i authd_0.5.3-0ubuntu24.04.1_amd64.deb
apt-get install -f -y
snap install authd-google

mkdir -p /etc/authd/brokers.d/
cp /snap/authd-google/current/conf/authd/google.conf /etc/authd/brokers.d/

chmod o-w /usr /bin /etc /var /tmp
chmod g-w /usr /bin /etc /var /tmp
chmod 711 /home

useradd -m -s /bin/bash student
echo 'student:$y$j9T$.rHm7.0/wgMukBMnf2wRL/$egvTyCS2HNa7Mq7og6eKYqOFSmNlJZBo8vK5EzJJrv3' | chpasswd -e # atFj5QNm3xgpctX8

mkdir -p /home/student/.config/gcloud/configurations
chmod -R 550 /home/student
chown -R student:student /home/student

touch /home/student/.config/gcloud/configurations/config_default
chown student:student /home/student/.config/gcloud/configurations/config_default
cat <<EOF > /home/student/.config/gcloud/configurations/config_default
[core]
account = admin@nusgreyhats.sg
project = <GOOGLE_OAUTH_CLIENT_ID>

[iam]
region = asia-southeast1
zone = asia-southeast1
EOF
chattr -R +i /home/student

grep -q '^KbdInteractiveAuthentication' /etc/ssh/sshd_config && sed -i 's/^#\?KbdInteractiveAuthentication.*/KbdInteractiveAuthentication yes/' /etc/ssh/sshd_config || echo 'KbdInteractiveAuthentication yes' >> /etc/ssh/sshd_config

sed -i -e "s|^client_id *=.*|client_id = ${OIDC_CLIENT_ID}|" -e "s|^client_secret *=.*|client_secret = ${OIDC_CLIENT_SECRET}|" -e "s|^#\?allowed_users *=.*|allowed_users = ALL|" -e "\$a ssh_allowed_suffixes = @gmail.com" /var/snap/authd-google/current/broker.conf

echo $FLAG > /flag
chmod 600 /flag
cat <<EOF > /printflag.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 256

int main(int argc, char *argv[]) {
    char date_output[MAX_LEN];
    FILE *fp = popen("date", "r");
    if (fp == NULL) {
        perror("popen failed");
        return 1;
    }

    if (fgets(date_output, sizeof(date_output), fp) == NULL) {
        perror("fgets from date failed");
        pclose(fp);
        return 1;
    }
    date_output[strlen(date_output) - 1] = '\0';
    pclose(fp);

    printf("What is the date?\n");
    char input[MAX_LEN];
    if (fgets(input, sizeof(input), stdin) == NULL) {
        perror("fgets from stdin failed");
        return 1;
    }

    if (strcmp(input, date_output) == 0) {
        printf("Thank you! ");
        FILE *file = fopen("/flag", "r");
        if (file == NULL) {
            perror("fopen failed");
            return 1;
        }

        char ch;
        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);
        }
        fclose(file);
    } else {
        printf("Sorry, the date is %s\n", date_output);
    }

    return 0;
}
EOF
chmod 640 /printflag.c

#gcc -o /printflag /printflag.c
chmod 710 /printflag # double check permissions
chmod a+s /printflag

systemctl restart authd
snap restart authd-google
systemctl restart ssh

