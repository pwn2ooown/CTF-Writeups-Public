#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/ioctl.h>
#include <linux/uaccess.h>

#define K1_TYPE 0xB9

#define ALLOC _IOW(K1_TYPE, 0, size_t)
#define FREE _IO(K1_TYPE, 1)
#define USE_READ _IOR(K1_TYPE, 2, char)
#define USE_WRITE _IOW(K1_TYPE, 2, char)

long handle_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

struct file_operations fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = handle_ioctl,
};

struct miscdevice vuln_dev ={
    .minor = MISC_DYNAMIC_MINOR,
    .name = "vuln",
    .fops = &fops, 
};

void* buf = NULL;
size_t size = 0;

long handle_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    switch (cmd) {
        case ALLOC: {
            if (buf) {
                return -EFAULT;
            }
            ssize_t n =  copy_from_user(&size, (void*)arg, sizeof(size_t));
            if (n != 0) {
                return n;
            }
            buf = kzalloc(size, GFP_KERNEL);
            return 0;
        };
        case FREE: {
            if (!buf) {
                return -EFAULT;
            }
            kfree(buf);
            break;
        }
        case USE_READ: {
            if (!buf) {
                return -EFAULT;
            }
            return copy_to_user((char*)arg, buf, size);
        }

        case USE_WRITE: {
            if (!buf) {
                return -EFAULT;
            }
            return copy_from_user(buf, (char*)arg, size);
        }

        default: {
            break;
        }

    }
    return 0;
}

int32_t vuln_init(void) {
    int ret;
    
    ret = misc_register(&vuln_dev);
    if (ret) {
        printk(KERN_ERR "Failed to register device\n");
        return ret;
    }
    return 0;
}

void vuln_exit(void) {
    misc_deregister(&vuln_dev);
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("UIUCTF Inc.");
MODULE_DESCRIPTION("Vulnerable Kernel Module");  
module_init(vuln_init);
module_exit(vuln_exit);