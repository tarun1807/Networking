#include <windows.h>
#include <stdio.h>

int main()
{
    //windows type variables
	HANDLE	hCom; //Handle variable
	DWORD	rwlen; // read/write length

    char send[32];
    char receive[32]= {0};

    int port,n;
    char port_name[20];

    printf("Please input serial port number ");
    scanf("%d",&port);

	/*	Open COM device	*/

	sprintf( port_name, "\\\\.\\COM%d", port );

	hCom = CreateFile( port_name, GENERIC_READ|GENERIC_WRITE,
					0, 0, OPEN_EXISTING, 0, 0 );

        if( hCom==INVALID_HANDLE_VALUE )
        {
            printf( "\terror: COM%d is not available.\n", port );
            return -2;
        }



    DCB dcbSerialParams = {0};

    dcbSerialParams.DCBlength=sizeof(dcbSerialParams);

    if (!GetCommState(hCom, &dcbSerialParams))
    {
        printf("Unable to get the state of serial port");
    //error getting state
    }

    dcbSerialParams.BaudRate=CBR_9600;
    dcbSerialParams.ByteSize=8;
    dcbSerialParams.StopBits=ONESTOPBIT;
    dcbSerialParams.Parity=NOPARITY;

    if(!SetCommState(hCom, &dcbSerialParams))
    {
        printf("Unable to set serial port settings\n");
               //error setting serial port state
    }

    /* DCB optional part ends here */

    /* COMTIMEOUTS Optional Part but very usefull especially against ReadHAngs */

    COMMTIMEOUTS timeouts={0};

    timeouts.ReadIntervalTimeout=50;
    timeouts.ReadTotalTimeoutConstant=50;
    timeouts.ReadTotalTimeoutMultiplier=10;
    timeouts.WriteTotalTimeoutConstant=50;
    timeouts.WriteTotalTimeoutMultiplier=10;

    if(!SetCommTimeouts(hCom, &timeouts))
    {

        printf("Error setting Serial Port timeouts property\n");
        //error occureed. Inform user
    }

        printf("COM%d opened successfully\n",port);



        printf("enter a string to send via serial port\n");

        scanf("%s",send);



        n = strlen(send); //number of bytes to transmit

		//Sleep(2000);//wait 2 secs, it is totally not necessary

        WriteFile( hCom, send, n, &rwlen, 0 ); //send data through serial port
		printf("%d bytes of Data transmitted successfully\n",rwlen);

		int i;
		for(i=0;i<10;i++)
		{

        strset(receive,0);//clears the string buffer "receive"
		Sleep(1000);
		ReadFile( hCom, receive, sizeof(receive), &rwlen, 0 ); // read data from the serial port buffer of the OS
        printf("%d of out of %d bytes read from port and data is %s\n",rwlen,sizeof(receive),receive);
		}


	CloseHandle( hCom );//close the handle

	return 0;
}
