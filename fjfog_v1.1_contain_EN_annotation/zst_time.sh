int=1
while(( $int<=5 ))
do
a=$(date "+%Y%m%d%H%M")
time_1=${a:9:11}
time_1=505
if [ $time_1 -gt 10 ] && [ $time_1 -lt 20 ]
then
b=$(date "+%Y%m%d%H%M")
zst_time=${b:2:10}"00.000"
echo $zst_time > zst_time.txt
mkdir temp
#./haha.out
sleep 5
rm -r temp
else
	sleep 310
	continue
fi
sleep 310 
done
