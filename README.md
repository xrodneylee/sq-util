# **InfinitiesSoft Toolbox**


## Usage

### Sample
```
SSH:
  description: Generate SSH public and secret keys.
  input:
    KEY_LENGTH:
      name: key size (bits)
      type: combobox
      option:
        - 2048
        - 4096
    button:
      name: Generate
      type: button
      action: ssh-keygen -b $KEY_LENGTH -f id_rsa -N ''
  output:
    RESULT:
      name: result
      type: textarea
      content:
        - id_rsa
        - id_rsa.pub
```