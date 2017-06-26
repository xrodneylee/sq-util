# **InfinitiesSoft Toolbox**


## Usage

### Restriction
- `description` must be setting.
- `input` must be setting.
  - `button` must be setting, and only one button.
- `output` must be setting.

### Sample
```yaml
SSH:
  description: Generate SSH public and secret keys.
  input:
    KEY_LENGTH:
      name: key size (bits)
      type: combobox
      option:
        - 2048
        - 4096
    TYPE:
      name: type
      type: radio
      option:
        - rsa
        - dsa
    button:
      name: Generate
      type: button
      actions: 
        - ssh-keygen -b $KEY_LENGTH -t $TYPE -f id_rsa -N ''
  output:
    PUBLIC_KEY:
      name: public key
      type: textarea
      content: id_rsa.pub
    PRIVATE_KEY:
      name: private key
      type: textarea
      content: id_rsa
```

### Setting
- type
  - combobox
  - radio
  - text
  - password
  - textarea
  - number
  - email
  - button