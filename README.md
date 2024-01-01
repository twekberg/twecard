# twecard


Create A Virtualenv And Install Dependencies
--------------------------------------------

Run these commands::
  python -m venv twecard-env
  dos2unix twecard-env/scripts/activate
  source twecard-env/scripts/activate
  pip install pip -U # Latest pip


Archive
-------

Couldn't get vcard to work so wrote my own.
  pip install --upgrade vcard

  cp ../../BACKUP/GALAXY_S20_5G_PHONE/Download/Contacts.vcf Contacts.vcf
  sed -i 's/VERSION:2.1/VERSION:3.0/' Contacts.vcf
